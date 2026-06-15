from __future__ import annotations

from typing import Any, Dict, List


def dispatch_tool(name: str, args: Dict[str, Any]) -> Any:
    """Dispatch an MCP tool call to the corresponding server handler.

    This module is the single place where tool-name → implementation mapping lives.
    The gateway can stay thin by calling this function.
    """

    args = args or {}

    # Slice 3: Dynamic plugins
    if name == "plugins.list":
        from sros.utils.plugin_loader import discover_plugins

        plugins = [
            {
                "name": p.name,
                "display_name": p.display_name or p.name,
                "description": p.description,
                "path": str(p.path),
                "input_schema": p.input_schema,
            }
            for p in discover_plugins()
        ]
        return {"ok": True, "plugins": plugins, "count": len(plugins)}

    if name == "plugins.run":
        from sros.utils.plugin_loader import run_plugin

        plugin = str(args.get("name") or "").strip()
        if not plugin:
            raise ValueError("Missing required arg: name")
        plugin_args = args.get("args") or {}
        if not isinstance(plugin_args, dict):
            raise ValueError("args must be an object")
        value = run_plugin(plugin, dict(plugin_args))
        return {"ok": True, "plugin": plugin, "result": value}

    if name.startswith("plugin."):
        from sros.utils.plugin_loader import run_plugin

        plugin = name.split(".", 1)[1].strip()
        if not plugin:
            raise ValueError("Invalid plugin tool name")
        if not isinstance(args, dict):
            raise ValueError("Plugin arguments must be an object")
        value = run_plugin(plugin, dict(args))
        return {"ok": True, "plugin": plugin, "result": value}

    # Slice 3: Long-running tasks
    if name == "tasks.run_plugin_async":
        from sros.servers.tasks.handler import TasksHandler

        plugin = str(args.get("plugin") or "").strip()
        if not plugin:
            raise ValueError("Missing required arg: plugin")
        plugin_args = args.get("args") or {}
        if not isinstance(plugin_args, dict):
            raise ValueError("args must be an object")
        return TasksHandler().run_plugin_async(plugin=plugin, args=dict(plugin_args))

    if name == "tasks.get":
        from sros.servers.tasks.handler import TasksHandler

        task_id = str(args.get("task_id") or "").strip()
        if not task_id:
            raise ValueError("Missing required arg: task_id")
        return TasksHandler().get_task(task_id)

    if name == "tasks.list":
        from sros.servers.tasks.handler import TasksHandler

        return TasksHandler().list_tasks()

    if name == "tasks.wait":
        from sros.servers.tasks.handler import TasksHandler

        task_id = str(args.get("task_id") or "").strip()
        if not task_id:
            raise ValueError("Missing required arg: task_id")
        timeout_s = float(args.get("timeout_s", 30.0))
        return TasksHandler().wait_task(task_id, timeout_s=timeout_s)

    if name == "manuscript.find_gaps":
        from sros.servers.manuscript.handler import ManuscriptHandler

        return ManuscriptHandler().find_gaps(args.get("file_path", "draft.md"))

    if name == "manuscript.get_outline_tree":
        from sros.servers.manuscript.handler import ManuscriptHandler

        return ManuscriptHandler().get_outline_tree(args.get("file_path", "draft.md"))

    if name == "manuscript.get_file_sha256":
        from sros.servers.manuscript.handler import ManuscriptHandler

        file_path = str(args.get("file_path", "draft.md"))
        sha = ManuscriptHandler().get_file_sha256(file_path)
        return {"file_path": file_path, "sha256": sha}

    if name == "manuscript.index_figure_references":
        from sros.servers.manuscript.handler import ManuscriptHandler

        return ManuscriptHandler().index_figure_references(str(args.get("file_path") or "draft.md"))

    if name == "manuscript.insert_section":
        from sros.servers.manuscript.handler import ManuscriptHandler

        missing = [k for k in ("target", "content", "citations", "file_path") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        return ManuscriptHandler().insert_section(
            target=str(args["target"]),
            content=str(args["content"]),
            citations=list(args.get("citations") or []),
            file_path=str(args.get("file_path") or "draft.md"),
            expected_sha256=args.get("expected_sha256"),
        )

    if name == "manuscript.patch_draft":
        from sros.servers.manuscript.handler import ManuscriptHandler

        missing = [k for k in ("patches", "file_path") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        return ManuscriptHandler().patch_draft(
            patches=list(args.get("patches") or []),
            file_path=str(args.get("file_path") or "draft.md"),
            expected_sha256=args.get("expected_sha256"),
        )

    if name in {"manuscript.refactor", "manuscript.refactor_section"}:
        from sros.servers.manuscript.handler import ManuscriptHandler

        missing = [k for k in ("target", "content", "citations", "file_path") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        return ManuscriptHandler().refactor_section(
            target=str(args["target"]),
            content=str(args["content"]),
            citations=list(args.get("citations") or []),
            file_path=str(args.get("file_path") or "draft.md"),
            expected_sha256=args.get("expected_sha256"),
        )

    if name in {"ext.web_scrape", "ext.web-scrape"}:
        from sros.servers.ext.handler import ExtHandler

        url = str(args.get("url") or "").strip()
        if not url:
            raise ValueError("Missing required arg: url")
        timeout_s = float(args.get("timeout_s", args.get("timeout", 15.0)))
        return ExtHandler.web_scrape(url, timeout_s=timeout_s)

    if name == "rag.build":
        from sros.servers.rag.handler import RagHandler

        sources = list(args.get("sources") or args.get("source") or [])
        return RagHandler().build(sources=[str(s) for s in sources])

    if name == "rag.query":
        from sros.servers.rag.handler import RagHandler

        q = str(args.get("query") or "").strip()
        if not q:
            raise ValueError("Missing required arg: query")
        top_k = int(args.get("top_k", args.get("top-k", 5)))
        return RagHandler().query(query=q, top_k=top_k)

    if name in {"scholar.search", "scholar.search_papers"}:
        # Phase-1 alias of federated_search
        from sros.domain.schemas import SearchQuery
        from sros.servers.scholar.handler import ScholarHandler

        q = SearchQuery(
            query=str(args.get("query") or ""),
            max_results=int(args.get("max_results", args.get("max-results", 10))),
            filters=dict(args.get("filters", {}) or {}),
        )
        return ScholarHandler().federated_search(q)

    if name in {"scholar.zotero_sync", "scholar.zotero-sync"}:
        # Phase-1 MVP: insert placeholder citations + export bib
        import os
        from pathlib import Path

        from sros.domain.schemas import Citation
        from sros.servers.zotero.handler import ZoteroHandler

        keys = list(args.get("citekeys") or args.get("citekey") or [])
        keys = [str(k).strip() for k in keys if str(k).strip()]
        if not keys:
            raise ValueError("Missing required arg: citekeys")

        ws = os.getenv("SROS_WORKSPACE_DIR")
        if not ws:
            raise ValueError("SROS_WORKSPACE_DIR is not set")

        root = Path(ws)
        refs_dir = root / "references"
        (refs_dir / "pdfs").mkdir(parents=True, exist_ok=True)
        refs_dir.mkdir(parents=True, exist_ok=True)

        zot = ZoteroHandler()
        for ck in keys:
            zot.add_citation(
                Citation(
                    citekey=ck,
                    title=ck,
                    authors=["Unknown"],
                    year=2026,
                    journal="",
                    url="",
                    bibtex=(
                        "@article{" + ck + ",\n"
                        "  title={" + ck + "},\n"
                        "  author={Unknown},\n"
                        "  year={2026}\n"
                        "}\n"
                    ),
                )
            )

        bib_path = refs_dir / "zotero_library.bib"
        citations = zot.search_citations("")
        citations_sorted = sorted(citations, key=lambda c: c.citekey)
        bib_text = "\n".join([(c.bibtex or "").rstrip() for c in citations_sorted if (c.bibtex or "").strip()]) + "\n"
        bib_path.write_text(bib_text, encoding="utf-8")
        return {"ok": True, "citekeys": keys, "bib_path": str(bib_path)}

    if name == "scholar.federated_search":
        from sros.domain.schemas import SearchQuery
        from sros.servers.scholar.handler import ScholarHandler

        if "query" not in args:
            raise ValueError("Missing required arg: query")

        q = SearchQuery(
            query=str(args["query"]),
            max_results=int(args.get("max_results", 10)),
            filters=dict(args.get("filters", {}) or {}),
        )
        return ScholarHandler().federated_search(q)

    if name == "scholar.brainstorm_perspectives":
        from sros.servers.scholar.handler import ScholarHandler

        if "query" not in args:
            raise ValueError("Missing required arg: query")
        return ScholarHandler().brainstorm_perspectives(str(args["query"]))

    if name == "scholar.find_critiques":
        from sros.servers.scholar.handler import ScholarHandler

        if "paper_id" not in args:
            raise ValueError("Missing required arg: paper_id")
        return ScholarHandler().find_critiques(str(args["paper_id"]))

    if name == "memory.store_knowledge":
        from sros.domain.schemas import KnowledgeEdge
        from sros.servers.memory.handler import MemoryHandler

        missing = [k for k in ("nodes", "edges") if k not in args]
        if missing:
            raise ValueError(f"Missing required args: {missing}")

        nodes = list(args.get("nodes") or [])
        edges_in: List[Any] = list(args.get("edges") or [])
        edges = [KnowledgeEdge(**e) if isinstance(e, dict) else e for e in edges_in]
        ok = MemoryHandler().store_knowledge(nodes=nodes, edges=edges)
        return {"ok": bool(ok)}

    if name == "memory.query_knowledge":
        from sros.servers.memory.handler import MemoryHandler

        if "query" not in args:
            raise ValueError("Missing required arg: query")
        return MemoryHandler().query_knowledge(query=str(args["query"]), limit=int(args.get("limit", 10)))

    if name in {"db.ingest", "db.ingest_data"}:
        from sros.servers.db.handler import DBHandler

        source = str(args.get("source") or "")
        if not source:
            raise ValueError("Missing required arg: source")
        handler = DBHandler(str(args.get("db_path", "sxmu.duckdb")))
        try:
            return handler.ingest(
                source_dir=source,
                bids_dir=args.get("bids_dir"),
                participants=args.get("participants"),
                clinical=args.get("clinical"),
                schema_path=args.get("schema"),
            )
        finally:
            handler.close()

    if name in {"db.query", "db.query_data"}:
        from sros.servers.db.handler import DBHandler

        sql = str(args.get("sql") or "").strip()
        if not sql:
            raise ValueError("Missing required arg: sql")
        handler = DBHandler(str(args.get("db_path", "sxmu.duckdb")))
        try:
            return handler.query(
                sql=sql,
                params=args.get("params"),
                limit=int(args.get("limit", 100)),
                offset=int(args.get("offset", 0)),
            )
        finally:
            handler.close()

    if name in {"hpc.submit", "hpc.submit_job"}:
        from sros.servers.hpc.handler import HPCHandler

        script = str(args.get("script_path") or args.get("script") or "")
        if not script:
            raise ValueError("Missing required arg: script_path")
        handler = HPCHandler(dry_run=bool(args.get("dry_run", False)))
        return handler.submit(
            script_path=script,
            array_size=args.get("array_size"),
        )

    if name in {"hpc.status", "hpc.job_status"}:
        from sros.servers.hpc.handler import HPCHandler

        job_id = str(args.get("job_id") or "")
        if not job_id:
            raise ValueError("Missing required arg: job_id")
        handler = HPCHandler(dry_run=bool(args.get("dry_run", False)))
        return handler.status(job_id=job_id)

    if name in {"hpc.cancel", "hpc.cancel_job"}:
        from sros.servers.hpc.handler import HPCHandler

        job_id = str(args.get("job_id") or "")
        if not job_id:
            raise ValueError("Missing required arg: job_id")
        handler = HPCHandler(dry_run=bool(args.get("dry_run", False)))
        return handler.cancel(job_id=job_id)

    if name in {"hpc.list", "hpc.list_jobs"}:
        from sros.servers.hpc.handler import HPCHandler

        handler = HPCHandler(dry_run=bool(args.get("dry_run", False)))
        return handler.list_jobs(user=args.get("user"))

    if name in {"hpc.logs", "hpc.job_logs"}:
        from sros.servers.hpc.handler import HPCHandler

        job_id = str(args.get("job_id") or "")
        if not job_id:
            raise ValueError("Missing required arg: job_id")
        handler = HPCHandler()
        return handler.logs(job_id=job_id, log_dir=str(args.get("log_dir", ".")))

    if name in {"hpc.generate", "hpc.generate_job"}:
        from sros.servers.hpc.handler import HPCHandler

        template = str(args.get("template") or args.get("template_path") or "")
        subject = str(args.get("subject") or args.get("subject_id") or "")
        if not template or not subject:
            raise ValueError("Missing required args: template, subject")
        handler = HPCHandler(dry_run=True)
        return handler.generate_job_script(
            template_path=template,
            subject_id=subject,
            output_dir=str(args.get("output_dir", ".")),
            substitutions=args.get("substitutions"),
        )

    if name == "memory.get_citation_map":
        from sros.servers.memory.handler import MemoryHandler

        if "section_id" not in args:
            raise ValueError("Missing required arg: section_id")
        return MemoryHandler().get_citation_map(section_id=str(args["section_id"]))

    if name in {"neuro.validate", "neuro.validate_bids"}:
        from sros.servers.neuro.handler import NeuroHandler

        bids_dir = str(args.get("bids_dir") or args.get("bids-dir") or "")
        if not bids_dir:
            raise ValueError("Missing required arg: bids_dir")
        return NeuroHandler().validate_bids(bids_dir, use_validator=bool(args.get("use_validator", False)))

    if name in {"neuro.generate_graphmri", "neuro.generate-graphmri"}:
        from sros.servers.neuro.handler import NeuroHandler

        subject = str(args.get("subject_id") or args.get("subject") or "")
        bids_dir = str(args.get("bids_dir") or args.get("bids-dir") or "")
        output_dir = str(args.get("output_dir") or args.get("output-dir") or "")
        if not all([subject, bids_dir, output_dir]):
            raise ValueError("Missing required args: subject_id, bids_dir, output_dir")
        config = args.get("config")
        matrices = args.get("connectivity_matrices") or args.get("matrices")
        return NeuroHandler().generate_graphmri_script(
            subject_id=subject,
            bids_dir=bids_dir,
            output_dir=output_dir,
            config=config,
            connectivity_matrices=matrices,
        )

    if name in {"neuro.generate_fmriprep", "neuro.generate-fmriprep"}:
        from sros.servers.neuro.handler import NeuroHandler

        subject_ids = list(args.get("subject_ids") or args.get("subjects") or [])
        if not subject_ids:
            raise ValueError("Missing required arg: subject_ids")
        bids_dir = str(args.get("bids_dir") or args.get("bids-dir") or "")
        output_dir = str(args.get("output_dir") or args.get("output-dir") or "")
        if not bids_dir or not output_dir:
            raise ValueError("Missing required args: bids_dir, output_dir")
        return NeuroHandler().generate_fmriprep_batch(
            subject_ids=[str(s) for s in subject_ids],
            bids_dir=bids_dir,
            output_dir=output_dir,
            work_dir=args.get("work_dir"),
            fs_license=args.get("fs_license"),
            template=args.get("template"),
        )

    raise NotImplementedError(f"Tool not implemented: {name}")
