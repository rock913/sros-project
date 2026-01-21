"""Analytics module for Phase 3.5.3.

Provides aggregated statistics and trends analysis for research sessions,
papers, and overall system performance.
"""

from datetime import datetime, timedelta
from typing import Any, Dict
from uuid import UUID

from sqlalchemy import and_, case, desc, func
from sqlalchemy.orm import joinedload

from agent.db_manager import get_db
from agent.models import Paper, Session, SessionEvent


def get_sessions_list(
    limit: int = 50,
    offset: int = 0,
    status: str | None = None,
    user_id: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc"
) -> Dict[str, Any]:
    """Get paginated list of sessions with optional filtering.
    
    Args:
        limit: Maximum number of results (1-200)
        offset: Number of records to skip
        status: Filter by session status (active/completed/archived)
        user_id: Filter by user ID
        sort_by: Sort field (created_at, duration, papers_count)
        order: Sort order (asc/desc)
    
    Returns:
        Dict with sessions list, total count, and pagination info
    """
    with get_db() as db:
        # Base query with relationships for efficient loading
        query = db.query(Session).options(
            joinedload(Session.papers),
            joinedload(Session.events)
        )
        
        # Apply filters
        filters = []
        if status:
            filters.append(Session.status == status)
        if user_id:
            # Assuming user_id is stored in session metadata or notes
            # Adjust based on actual schema
            filters.append(Session.notes.contains(user_id))
        
        if filters:
            query = query.filter(and_(*filters))
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        if sort_by == "created_at":
            sort_column = Session.created_at
        elif sort_by == "duration":
            # Calculate duration as (completed_at - created_at)
            sort_column = (Session.completed_at - Session.created_at)
        elif sort_by == "papers_count":
            # This requires a subquery or post-processing
            # For now, sort by created_at and we'll handle papers_count in Python
            sort_column = Session.created_at
        else:
            sort_column = Session.created_at
        
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)
        
        # Apply pagination
        sessions = query.limit(limit).offset(offset).all()
        
        # Convert to dict with calculated fields
        session_list = []
        for s in sessions:
            session_dict = {
                'session_id': str(s.id),
                'thread_id': str(s.thread_id),
                'title': s.title,
                'research_topic': s.research_topic,
                'status': s.status,
                'created_at': s.created_at.isoformat() if s.created_at else None,
                'completed_at': s.completed_at.isoformat() if s.completed_at else None,
                'papers_count': len(s.papers),
                'events_count': len(s.events),
                'tags': s.tags or [],
            }
            
            # Calculate duration
            if s.completed_at and s.created_at:
                duration = (s.completed_at - s.created_at).total_seconds()
                session_dict['duration_seconds'] = duration
            else:
                session_dict['duration_seconds'] = None
            
            session_list.append(session_dict)
        
        # Sort by papers_count if requested (post-processing)
        if sort_by == "papers_count":
            session_list.sort(
                key=lambda x: x['papers_count'],
                reverse=(order == "desc")
            )
        
        return {
            'sessions': session_list,
            'total': total,
            'limit': limit,
            'offset': offset,
            'has_more': (offset + limit) < total
        }


def get_session_details(session_id: UUID) -> Dict[str, Any] | None:
    """Get detailed analytics for a specific session.
    
    Args:
        session_id: UUID of the session
    
    Returns:
        Dict with session info, events, and timeline analysis
        None if session not found
    """
    with get_db() as db:
        session = db.query(Session).filter(Session.id == session_id).first()
        
        if not session:
            return None
        
        # Get all events ordered by timestamp
        events = db.query(SessionEvent).filter(
            SessionEvent.session_id == session_id
        ).order_by(SessionEvent.created_at).all()
        
        # Build session summary
        session_dict = {
            'session_id': str(session.id),
            'thread_id': str(session.thread_id),
            'title': session.title,
            'research_topic': session.research_topic,
            'status': session.status,
            'created_at': session.created_at.isoformat() if session.created_at else None,
            'completed_at': session.completed_at.isoformat() if session.completed_at else None,
            'papers_count': len(session.papers),
            'tags': session.tags or [],
            'notes': session.notes,
        }
        
        # Calculate duration
        total_duration = 0
        if session.completed_at and session.created_at:
            total_duration = (session.completed_at - session.created_at).total_seconds()
            session_dict['duration_seconds'] = total_duration
        
        # Build events list
        events_list = [
            {
                'event_id': str(e.id),
                'session_id': str(e.session_id),
                'event_type': e.event_type,
                'timestamp': e.created_at.isoformat() if e.created_at else None,
                'metadata': e.event_data or {}
            }
            for e in events
        ]
        
        # Analyze timeline phases (simple heuristic)
        timeline = {'total_duration_seconds': total_duration, 'phases': []}
        
        if events and total_duration > 0:
            # Simple phase detection based on event types
            init_events = [e for e in events if 'start' in e.event_type.lower()]
            report_events = [e for e in events if 'report' in e.event_type.lower()]
            
            init_duration = 0
            report_duration = 0
            
            if init_events:
                init_end = init_events[-1].created_at
                init_duration = (init_end - session.created_at).total_seconds()
            
            if report_events:
                report_start = report_events[0].created_at
                report_duration = (session.completed_at - report_start).total_seconds()
            
            research_duration = total_duration - init_duration - report_duration
            
            timeline['phases'] = [
                {
                    'phase': 'initialization',
                    'duration_seconds': round(init_duration, 2),
                    'percentage': round((init_duration / total_duration) * 100, 1)
                },
                {
                    'phase': 'research',
                    'duration_seconds': round(research_duration, 2),
                    'percentage': round((research_duration / total_duration) * 100, 1)
                },
                {
                    'phase': 'report_generation',
                    'duration_seconds': round(report_duration, 2),
                    'percentage': round((report_duration / total_duration) * 100, 1)
                }
            ]
        
        return {
            'session': session_dict,
            'events': events_list,
            'timeline': timeline
        }


def get_sessions_stats(
    time_range: str = "7d",
    user_id: str | None = None
) -> Dict[str, Any]:
    """Get aggregated statistics across sessions.
    
    Args:
        time_range: Time window (24h, 7d, 30d, all)
        user_id: Optional user filter
    
    Returns:
        Dict with aggregated metrics, daily breakdown, and top topics
    """
    with get_db() as db:
        # Calculate time threshold
        now = datetime.utcnow()
        if time_range == "24h":
            threshold = now - timedelta(hours=24)
        elif time_range == "7d":
            threshold = now - timedelta(days=7)
        elif time_range == "30d":
            threshold = now - timedelta(days=30)
        else:  # all
            threshold = datetime(2000, 1, 1)
        
        # Base filter
        filters = [Session.created_at >= threshold]
        if user_id:
            filters.append(Session.notes.contains(user_id))
        
        # Aggregate stats
        stats_query = db.query(
            func.count(Session.id).label('total'),
            func.count(case((Session.status == 'completed', 1))).label('completed'),
            func.count(case((Session.status == 'failed', 1))).label('failed'),
            func.count(case((Session.status == 'active', 1))).label('running'),
        ).filter(and_(*filters))
        
        result = stats_query.first()
        
        total_sessions = result.total or 0
        completed_sessions = result.completed or 0
        failed_sessions = result.failed or 0
        running_sessions = result.running or 0
        
        success_rate = 0
        if total_sessions > 0:
            success_rate = (completed_sessions / total_sessions) * 100
        
        # Get all sessions for detailed calculations
        sessions = db.query(Session).options(
            joinedload(Session.papers)
        ).filter(and_(*filters)).all()
        
        total_papers = sum(len(s.papers) for s in sessions)
        avg_papers = total_papers / total_sessions if total_sessions > 0 else 0
        
        # Calculate average duration for completed sessions
        completed = [s for s in sessions if s.status == 'completed' and s.completed_at]
        durations = [
            (s.completed_at - s.created_at).total_seconds()
            for s in completed
            if s.created_at
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Daily breakdown
        daily_query = db.query(
            func.date(Session.created_at).label('date'),
            func.count(Session.id).label('sessions'),
            func.count(case((Session.status == 'completed', 1))).label('completed'),
            func.count(case((Session.status == 'failed', 1))).label('failed'),
        ).filter(and_(*filters)).group_by(
            func.date(Session.created_at)
        ).order_by(desc('date'))
        
        daily_breakdown = [
            {
                'date': str(row.date),
                'sessions': row.sessions,
                'completed': row.completed,
                'failed': row.failed,
            }
            for row in daily_query.all()
        ]
        
        # Top topics (extract from research_topic field)
        topic_query = db.query(
            Session.research_topic,
            func.count(Session.id).label('count')
        ).filter(
            and_(*filters),
            Session.research_topic.isnot(None)
        ).group_by(
            Session.research_topic
        ).order_by(desc('count')).limit(10)
        
        top_topics = [
            {
                'topic': row.research_topic,
                'count': row.count,
                'avg_papers': 0  # Could calculate per topic if needed
            }
            for row in topic_query.all()
        ]
        
        return {
            'time_range': time_range,
            'stats': {
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions,
                'failed_sessions': failed_sessions,
                'running_sessions': running_sessions,
                'success_rate': round(success_rate, 1),
                'total_papers_collected': total_papers,
                'avg_papers_per_session': round(avg_papers, 1),
                'avg_duration_seconds': round(avg_duration, 1),
            },
            'daily_breakdown': daily_breakdown,
            'top_topics': top_topics
        }


def get_papers_trends(time_range: str = "7d") -> Dict[str, Any]:
    """Analyze paper collection trends.
    
    Args:
        time_range: Time window (24h, 7d, 30d, all)
    
    Returns:
        Dict with paper trends, venue distribution, and year distribution
    """
    with get_db() as db:
        # Calculate time threshold
        now = datetime.utcnow()
        if time_range == "24h":
            threshold = now - timedelta(hours=24)
        elif time_range == "7d":
            threshold = now - timedelta(days=7)
        elif time_range == "30d":
            threshold = now - timedelta(days=30)
        else:  # all
            threshold = datetime(2000, 1, 1)
        
        # Papers created after threshold
        papers = db.query(Paper).filter(
            Paper.created_at >= threshold
        ).all()
        
        total_papers = len(papers)
        unique_dois = len(set(p.doi for p in papers if p.doi))
        
        # Papers by day
        daily_query = db.query(
            func.date(Paper.created_at).label('date'),
            func.count(Paper.id).label('papers_count')
        ).filter(
            Paper.created_at >= threshold
        ).group_by(
            func.date(Paper.created_at)
        ).order_by(desc('date'))
        
        papers_by_day = [
            {
                'date': str(row.date),
                'papers_count': row.papers_count
            }
            for row in daily_query.all()
        ]
        
        # Calculate average per day
        days_span = (now - threshold).days or 1
        avg_papers_per_day = total_papers / days_span if days_span > 0 else 0
        
        # Top venues (from extra_metadata if available)
        # This is a placeholder - adjust based on actual data structure
        top_venues = [
            {'venue': 'arXiv', 'papers_count': 0, 'percentage': 0},
        ]
        
        # Papers by publication year (from extra_metadata if available)
        papers_by_year = []
        
        return {
            'time_range': time_range,
            'trends': {
                'total_papers': total_papers,
                'unique_papers': unique_dois,
                'avg_papers_per_day': round(avg_papers_per_day, 1),
                'papers_by_day': papers_by_day,
                'top_venues': top_venues,
                'papers_by_year': papers_by_year
            }
        }
