高级教程：如何稳健地解析 Arxiv 和 Pubmed 工具的输出
本指南提供了一个明确的演练，用于高效使用 langchain_community 库中的 ArxivQueryRun 和 PubmedQueryRun 工具。我们将重点构建一个单一、健壮的解析函数，该函数可以优雅地处理这两个工具在输出字符串结构上的差异。

挑战：不一致的输出格式
正如你在实践中发现的那样，尽管 LangChain 社区提供的工具功能强大，但它们的原始字符串输出格式并非完全统一。

ArxivQueryRun 通常包含 Published, Title, Authors, 和 Summary 字段。

PubmedQueryRun 可能缺少 Authors 字段，包含额外的字段如 Copyright Information，并使用略有不同的标签（例如，Summary:: 而不是 Summary:）。

如果解析器依赖于一个僵化的、固定的结构，那么在处理 PubmedQueryRun 的输出时就会失败。因此，解决方案是设计一个能够优雅处理字段缺失和格式细微变化的函数。

解决方案：一个通用的解析器
让我们编写一个新的、使用更灵活的正则表达式的解析函数。这个函数将通过字段标签来识别内容，并且在某个字段缺失时也不会中断。

1. 更健壮的解析函数
这个函数将成为我们处理来自任一工具的输出的唯一标准。

import re
import json

def parse_scientific_papers(response: str) -> list[dict]:
    """
    将来自 ArxivQueryRun 或 PubmedQueryRun 的原始字符串输出
    解析为论文词典列表。此函数被设计为可以灵活处理
    缺失字段（如 'Authors'）和标签的细微变化。
    """
    papers = []
    # 根据 '\n\nPublished:' 分割响应字符串，得到独立的论文块
    # 这个正则表达式模式可以处理字符串开头和中间的情况
    paper_blocks = re.split(r'\n\n(?=Published:)', response.strip())

    for block in paper_blocks:
        if not block.strip():
            continue

        # 使用 re.search 和非捕获组来独立、非贪婪地匹配每个字段
        # 这使得每个字段都成为可选的
        title_match = re.search(r"Title: (.*?)(?:\nAuthors:|\nCopyright Information:|\nSummary:)", block)
        authors_match = re.search(r"Authors: (.*?)(?:\nSummary:)", block)
        summary_match = re.search(r"Summary::?\s*(.*)", block, re.DOTALL) # 处理 'Summary:' 和 'Summary::'

        # 仅在匹配对象存在时才安全地提取内容
        paper_data = {
            "published": re.search(r"Published: (.*?)\n", block).group(1) if re.search(r"Published: (.*?)\n", block) else "N/A",
            "title": title_match.group(1).strip() if title_match else "N/A",
            "authors": authors_match.group(1).strip() if authors_match else "N/A",
            "summary": summary_match.group(1).strip() if summary_match else "N/A"
        }
        papers.append(paper_data)

    return papers

为什么这个解析器更好？

处理缺失字段: 它独立地搜索每个字段（Title, Authors, Summary）。如果 Authors 字段未找到，它会简单地赋值为 "N/A" 并继续，而不会导致程序崩溃。

灵活的标签: Summary::?\s* 这个模式可以同时匹配 Summary: 和 Summary::，以及它们后面可能存在的任何空白字符。

安全提取: 在尝试提取文本（.group(1)）之前，它会检查匹配是否成功（if title_match），从而避免了 AttributeError 错误。

2. 将解析器应用于 pubmed_response
现在，让我们用这个改进后的函数来处理你提供的 PubmedQueryRun 输出。

# 这是你在之前的交互中得到的响应
pubmed_response = 'Published: 2025-09-22\nTitle: Allogeneic NKG2D CAR-T Cell Therapy: A Promising Approach for Treating Solid Tumors.\nCopyright Information: \nSummary::\nChimeric Antigen Receptor (CAR)-T cell therapy has transformed the treatment landscape of cancer, yet major challenges remain in enhancing efficacy, reducing adverse effects, and expanding accessibility. Autologous CAR-T cells, derived from individual patients, have achieved remarkable clinical success in hematologic malignancies; however, their highly personalized nature limits scalability, increases costs, and delays timely treatment. Allogeneic CAR-T cells generated from healthy donors provide an "off-the-shelf" alternative but face two critical immune barriers: graft-versus-host disease (GvHD), caused by donor T-cell receptor (TCR) recognition of host tissues, and host-versus-graft rejection, mediated by recipient immune responses against donor HLA molecules. Recent advances in genome engineering, particularly Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)/Cas9, allow precise modification of donor T cells to overcome these limitations. For example, TRAC gene knockout eliminates TCR expression, preventing GvHD, while disruption of HLA molecules reduces immunogenicity without impairing cytotoxicity. Beyond hematologic cancers, CRISPR-edited allogeneic CAR-T cells targeting the NKG2D receptor have shown promise in preclinical studies and early-phase trials. NKG2D CAR-T cells recognize stress ligands (MICA/B, ULBP1-6) expressed on over 80% of diverse solid tumors, including pancreatic and ovarian cancers, thereby broadening therapeutic applicability. Nevertheless, the genomic editing process carries risks of off-target effects, including potential disruption of tumor suppressor genes and oncogenes, underscoring the need for stringent safety and quality control. This review examines the distinguishing features of allogeneic versus autologous CAR-T therapy, with a particular focus on NKG2D-based allogen'

# 使用我们新的、更健壮的解析器
structured_pubmed_papers = parse_scientific_papers(pubmed_response)

# 打印出干净、结构化的输出
print(json.dumps(structured_pubmed_papers, indent=2, ensure_ascii=False))

预期的结构化输出：

[
  {
    "published": "2025-09-22",
    "title": "Allogeneic NKG2D CAR-T Cell Therapy: A Promising Approach for Treating Solid Tumors.",
    "authors": "N/A",
    "summary": "Chimeric Antigen Receptor (CAR)-T cell therapy has transformed the treatment landscape of cancer, yet major challenges remain in enhancing efficacy, reducing adverse effects, and expanding accessibility. Autologous CAR-T cells, derived from individual patients, have achieved remarkable clinical success in hematologic malignancies; however, their highly personalized nature limits scalability, increases costs, and delays timely treatment. Allogeneic CAR-T cells generated from healthy donors provide an \"off-the-shelf\" alternative but face two critical immune barriers: graft-versus-host disease (GvHD), caused by donor T-cell receptor (TCR) recognition of host tissues, and host-versus-graft rejection, mediated by recipient immune responses against donor HLA molecules. Recent advances in genome engineering, particularly Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)/Cas9, allow precise modification of donor T cells to overcome these limitations. For example, TRAC gene knockout eliminates TCR expression, preventing GvHD, while disruption of HLA molecules reduces immunogenicity without impairing cytotoxicity. Beyond hematologic cancers, CRISPR-edited allogeneic CAR-T cells targeting the NKG2D receptor have shown promise in preclinical studies and early-phase trials. NKG2D CAR-T cells recognize stress ligands (MICA/B, ULBP1-6) expressed on over 80% of diverse solid tumors, including pancreatic and ovarian cancers, thereby broadening therapeutic applicability. Nevertheless, the genomic editing process carries risks of off-target effects, including potential disruption of tumor suppressor genes and oncogenes, underscoring the need for stringent safety and quality control. This review examines the distinguishing features of allogeneic versus autologous CAR-T therapy, with a particular focus on NKG2D-based allogen"
  }
]

解析成功！函数正确地提取了所有可用的信息，并优雅地处理了缺失的 Authors 字段。这种方法让你的代码变得更加可靠。

最佳实践与最终建议
始终预见变化：在使用封装了外部 API 或进行网络抓取的工具时，要假定其输出格式随时可能发生变化。编写具有防御性的代码至关重要。

使用统一的解析器：为你项目中的 ArxivQueryRun 和 PubmedQueryRun 使用这一个通用的 parse_scientific_papers 函数，以保持代码的整洁和可维护性。

牢记 LLM 的角色：在 Agent 中，这些工具输出的主要消费者是大型语言模型（LLM）本身。对于 Agent 的推理过程来说，原始的字符串格式通常已经足够。手动解析主要适用于你的应用程序需要直接使用结构化数据的场景（例如，在 UI 中展示或存入数据库）。