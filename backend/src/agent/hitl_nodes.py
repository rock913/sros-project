"""
Human-in-the-Loop (HITL) Node Implementation

Phase 3.6: HITL Decision Points
- query_approval: User reviews and approves/modifies generated queries
- paper_selection: User selects which papers to focus on
- report_revision: User reviews and provides feedback on generated report

Author: Development Team
Date: 2025-10-14
"""

import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from langchain_core.runnables import RunnableConfig

from langchain_core.messages import AIMessage
from agent.state import AgentState
from agent.database import get_db_connection
from agent.models import HITLDecision


def create_hitl_request(
    session_id: str,
    decision_type: str,
    prompt: str,
    options: list,
    context: Optional[Dict[str, Any]] = None,
    timeout_seconds: int = 300
) -> str:
    """
    Create a HITL decision request and store it in database
    
    Args:
        session_id: Session UUID
        decision_type: Type of decision (query_approval, paper_selection, report_revision)
        prompt: Question/prompt to show to user
        options: List of available options
        context: Additional context data for display
        timeout_seconds: Timeout in seconds (default 5 minutes)
    
    Returns:
        request_id: Unique identifier for this HITL request
    """
    request_id = f"hitl_{decision_type}_{uuid.uuid4().hex[:8]}"
    
    with get_db_connection() as session:
        hitl_decision = HITLDecision(
            id=uuid.uuid4(),
            session_id=uuid.UUID(session_id),
            request_id=request_id,
            decision_type=decision_type,
            prompt=prompt,
            options=options,
            context=context,
            timeout_seconds=timeout_seconds,
            created_at=datetime.utcnow()
        )
        session.add(hitl_decision)
        session.commit()
    
    return request_id


def query_approval_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
    """
    HITL Node 1: Query Approval
    
    Pauses execution and asks user to approve/reject/modify generated queries.
    This node triggers when initial queries have been generated.
    
    Flow:
    1. Extract generated queries from state
    2. Create HITL request in database
    3. Send WebSocket message to frontend (via state update)
    4. Wait for user response (interrupt execution)
    5. Resume with user's decision
    """
    queries = state.get("search_queries", [])  # Use correct state field name
    research_topic = state.get("research_topic", "")
    session_id = state.get("session_id")
    
    # Check if user has already responded (resuming from interrupt)
    hitl_response = state.get("hitl_response")
    if hitl_response:
        decision = hitl_response.get("user_decision")  # Consistent with other nodes
        modified_data = hitl_response.get("modified_data")
        
        if decision == "approve":
            return {
                "messages": [AIMessage(content="✅ User approved queries")],
                "hitl_approved": True,
                "hitl_pending": False,
                "hitl_response": None
            }
        elif decision == "reject":
            return {
                "messages": [AIMessage(content="❌ User rejected queries, terminating")],
                "hitl_approved": False,
                "hitl_pending": False,
                "hitl_response": None,
                "stop_research": True
            }
        elif decision == "modify" and modified_data:
            # User provided modified queries
            modified_queries = modified_data.get("queries", queries)
            return {
                "search_queries": modified_queries,  # Use correct state field
                "messages": [AIMessage(content=f"✏️ User modified queries: {modified_queries}")],
                "hitl_approved": True,
                "hitl_pending": False,
                "hitl_response": None
            }
    
    # First time reaching this node - create HITL request
    request_id = create_hitl_request(
        session_id=session_id,
        decision_type="query_approval",
        prompt=f"AI已为研究主题「{research_topic}」生成以下查询，是否继续？",
        options=["approve", "reject", "modify"],
        context={
            "research_topic": research_topic,
            "queries": queries,
            "query_count": len(queries)
        },
        timeout_seconds=300  # 5 minutes
    )
    
    # Update state with HITL request info (will be sent via WebSocket)
    return {
        "messages": [AIMessage(content=f"⏸️ Waiting for user approval (request: {request_id})")],
        "hitl_request": {
            "request_id": request_id,
            "type": "query_approval",
            "prompt": f"AI已为研究主题「{research_topic}」生成以下查询，是否继续？",
            "options": ["approve", "reject", "modify"],
            "context": {
                "research_topic": research_topic,
                "queries": queries
            }
        },
        "hitl_pending": True  # Signal to interrupt execution
    }


def paper_selection_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
    """
    HITL Point 2: Paper Selection
    
    当搜索到的论文数量 > 20 时触发人工选择
    用户从列表中选择要深入分析的论文
    
    Workflow:
    1. 首次调用: 检查论文数量，如果 >20 则创建 HITL 请求并返回 hitl_pending=True
    2. 用户响应后: graph.aupdate_state() 注入 hitl_response
    3. 二次调用: 检测到 hitl_response，处理用户选择，返回 selected_papers
    
    Args:
        state: Current agent state with literature_abstracts
        config: LangGraph config with thread_id
    
    Returns:
        Dict with paper_selection_done=True or hitl_pending=True
    """
    session_id = state.get("session_id")
    
    # Check if already responded (second execution after user response)
    if check_hitl_response(state, "paper_selection"):
        hitl_response = state.get("hitl_response", {})
        decision = hitl_response.get("user_decision")
        
        if decision == "select_all":
            # User wants to analyze all papers
            papers = state.get("literature_abstracts", [])
            return {
                "selected_papers": papers,
                "paper_selection_done": True,
                "hitl_pending": False,
                "hitl_response": None,
                "hitl_approved": True
            }
        
        elif decision == "select_subset":
            # User provided custom selection
            selected_papers = hitl_response.get("modified_data", {}).get("selected_papers", [])
            return {
                "selected_papers": selected_papers,
                "paper_selection_done": True,
                "hitl_pending": False,
                "hitl_response": None,
                "hitl_approved": True
            }
        
        elif decision == "reject":
            # User rejects all papers, stop research
            return {
                "stop_research": True,
                "paper_selection_done": True,
                "hitl_pending": False,
                "hitl_response": None
            }
    
    # Check if HITL is needed (papers > 20)
    papers = state.get("literature_abstracts", [])
    
    if len(papers) <= 20:
        # Small paper set, no need for HITL
        return {
            "selected_papers": papers,
            "paper_selection_done": True
        }
    
    # First execution: Create HITL request
    research_topic = state.get("research_topic", "")
    
    request_id = create_hitl_request(
        session_id=session_id,
        decision_type="paper_selection",
        prompt=f"发现 {len(papers)} 篇论文。请选择要深入分析的论文：",
        options=["select_all", "select_subset", "reject"],
        context={
            "research_topic": research_topic,
            "total_count": len(papers),
            "papers": [
                {
                    "title": p.get("title", "Untitled"),
                    "authors": p.get("authors", []),
                    "year": p.get("year"),
                    "doi": p.get("doi"),
                    "abstract": p.get("abstract", "")[:200] + "..."  # Truncate abstract
                }
                for p in papers[:50]  # Max 50 papers in UI
            ],
            "recommendation": "建议选择 10-20 篇最相关的论文进行深入分析"
        },
        timeout_seconds=600  # 10 minutes timeout
    )
    
    return {
        "hitl_pending": True,
        "hitl_request": {
            "request_id": request_id,
            "type": "paper_selection",  # Consistent with query_approval_node
            "prompt": f"发现 {len(papers)} 篇论文。请选择要深入分析的论文：",
            "options": ["select_all", "select_subset", "reject"],
            "context": {
                "total_count": len(papers),
                "papers": [
                    {
                        "title": p.get("title", "Untitled"),
                        "authors": p.get("authors", []),
                        "year": p.get("year"),
                        "doi": p.get("doi"),
                        "abstract": p.get("abstract", "")[:200] + "..."
                    }
                    for p in papers[:50]
                ]
            },
            "timeout_seconds": 600
        }
    }


def report_revision_node(state: AgentState, config: RunnableConfig) -> Dict[str, Any]:
    """
    HITL Point 3: Report Revision
    
    用户审核生成的研究报告，可以：
    1. 接受报告 (approve)
    2. 提供修改建议 (modify)
    3. 拒绝报告，终止研究 (reject)
    
    Workflow:
    1. 首次调用: 创建 HITL 请求，展示报告内容
    2. 用户响应后: 处理决策
       - approve: 直接使用报告
       - modify: 附加用户反馈到报告（未来可接入 LLM 重写）
       - reject: 终止研究
    
    Args:
        state: Current agent state with report
        config: LangGraph config
    
    Returns:
        Dict with final_report or stop_research flag
    """
    session_id = state.get("session_id")
    
    # Check if already responded
    if check_hitl_response(state, "report_revision"):
        hitl_response = state.get("hitl_response", {})
        decision = hitl_response.get("user_decision")
        
        if decision == "approve":
            # User approves report as-is
            return {
                "final_report": state.get("report", ""),
                "hitl_pending": False,
                "hitl_response": None,
                "hitl_approved": True
            }
        
        elif decision == "modify":
            # User provides feedback for modification
            feedback = hitl_response.get("modified_data", {}).get("feedback", "")
            original_report = state.get("report", "")
            
            # Phase 3.6: Simple append feedback
            # Phase 3.7: Can integrate LLM to rewrite based on feedback
            modified_report = original_report + f"\n\n## User Feedback\n{feedback}"
            
            return {
                "final_report": modified_report,
                "hitl_pending": False,
                "hitl_response": None,
                "hitl_approved": True
            }
        
        elif decision == "reject":
            # User rejects report, stop research
            return {
                "stop_research": True,
                "hitl_pending": False,
                "hitl_response": None
            }
    
    # First execution: Create HITL request
    report = state.get("report", "")
    word_count = len(report.split())
    research_topic = state.get("research_topic", "")
    
    request_id = create_hitl_request(
        session_id=session_id,
        decision_type="report_revision",
        prompt="请审核生成的研究报告：",
        options=["approve", "modify", "reject"],
        context={
            "report": report,
            "word_count": word_count,
            "research_topic": research_topic,
            "paper_count": len(state.get("literature_abstracts", []))
        },
        timeout_seconds=900  # 15 minutes timeout
    )
    
    return {
        "hitl_pending": True,
        "hitl_request": {
            "request_id": request_id,
            "type": "report_revision",  # Consistent with other nodes
            "prompt": "请审核生成的研究报告：",
            "options": ["approve", "modify", "reject"],
            "context": {
                "report": report,
                "word_count": word_count,
                "research_topic": research_topic,
                "paper_count": len(state.get("literature_abstracts", []))
            },
            "timeout_seconds": 900
        }
    }


def check_hitl_response(state: AgentState, decision_type: str) -> bool:
    """
    Helper function to check if user has responded to a specific HITL request
    
    Args:
        state: Current agent state
        decision_type: Type of HITL decision to check (query_approval, paper_selection, report_revision)
    
    Returns:
        True if user has responded with matching decision_type, False otherwise
    """
    hitl_response = state.get("hitl_response")
    if not hitl_response:
        return False
    
    # Check if response matches the decision type we're looking for
    response_type = hitl_response.get("decision_type")
    return response_type == decision_type
