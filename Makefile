.PHONY: update-wiki update-wiki-dry-run check-wiki test lint

# ── Code-Wiki 架构图谱更新 ──────────────────────────────────────────────
# 依赖 ARC Engine 的 claw-code-ingest CLI。
# 安装: pip install arc-engine (或通过 ARC-Engine 仓库安装)

update-wiki:
	@echo "==> Calling ARC to refresh SROS Code-Wiki..."
	@export PATH="$$HOME/.local/bin:$$PATH" && which claw-code-ingest >/dev/null 2>&1 || { \
		echo "ERROR: claw-code-ingest not found. Install ARC Engine first:"; \
		echo "  pip install -e ../ARC-Engine"; \
		exit 1; \
	}
	@export PATH="$$HOME/.local/bin:$$PATH" && claw-code-ingest --pretty --input - < arc_wiki.json
	git add docs/code_wiki/
	@echo "==> Code-Wiki updated and staged."

update-wiki-dry-run:
	@echo "==> [DRY-RUN] Calling ARC to refresh SROS Code-Wiki..."
	@export PATH="$$HOME/.local/bin:$$PATH" && which claw-code-ingest >/dev/null 2>&1 || { \
		echo "ERROR: claw-code-ingest not found. Install ARC Engine first:"; \
		echo "  pip install -e ../ARC-Engine"; \
		exit 1; \
	}
	@export PATH="$$HOME/.local/bin:$$PATH" && echo '{"vault_dir":".","raw_dir":"src/sros","wiki_dir":"docs/code_wiki","git_diff_since":":state","dry_run":true}' | claw-code-ingest --pretty --input -
	@echo "==> [DRY-RUN] Done. No files modified."

check-wiki:
	@if [ ! -d docs/code_wiki ]; then \
		echo "ERROR: docs/code_wiki/ not found. Run: make update-wiki"; \
		exit 1; \
	fi
	@newest_src=$$(find src/sros -name '*.py' -type f -exec stat -c '%Y' {} \; 2>/dev/null | sort -rn | head -1); \
	newest_wiki=$$(find docs/code_wiki -type f -exec stat -c '%Y' {} \; 2>/dev/null | sort -rn | head -1); \
	if [ -z "$$newest_wiki" ]; then \
		echo "WARNING: docs/code_wiki/ is empty. Run: make update-wiki"; \
		exit 1; \
	fi; \
	if [ "$$newest_src" -gt "$$newest_wiki" ]; then \
		echo "WARNING: Source code is newer than Code-Wiki. Run: make update-wiki"; \
		echo "  src/sros/ newest: $$(date -d @$$newest_src 2>/dev/null || date -r $$newest_src 2>/dev/null)"; \
		echo "  docs/code_wiki/ newest: $$(date -d @$$newest_wiki 2>/dev/null || date -r $$newest_wiki 2>/dev/null)"; \
		exit 1; \
	fi; \
	echo "Code-Wiki is up to date."

# ── 开发辅助 ─────────────────────────────────────────────────────────────

test:
	pytest tests/ -v -m "not integration"

test-integration:
	pytest tests/ -v -m "integration"

test-all:
	pytest tests/ -v

lint:
	flake8 src/sros/
	mypy src/sros/ --ignore-missing-imports
	@$(MAKE) --no-print-directory check-wiki
