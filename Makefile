.PHONY: help code-web docs-openapi docs-openapi-check docs-check

help: ## List the targets in this file
	@grep -hE '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | sed 's/:.*## /\t/'

docs-openapi: ## Generate docs/reference/openapi.json and routes.md from the code
	uv run scripts/docs_openapi_cli.py

docs-openapi-check: ## Fail when the generated reference is older than the code
	uv run scripts/docs_openapi_check_cli.py

docs-check: ## Build the docs strictly, check links offline, check the generated reference
	uvx --from 'mkdocs==1.6.1' mkdocs build --strict --site-dir site
	uvx --from lychee-bin lychee --offline --include-fragments --exclude-path 'docs/templates' README.md docs
	$(MAKE) docs-openapi-check

.PHONY: code-web

CODE_WEB_PORT ?= 8888
CODE_WEB_DIR := $(CURDIR)/.vscode-web
CODE_WEB_WORKSPACE := $(CODE_WEB_DIR)/project.code-workspace
CODE_WEB_TOKEN := $(CODE_WEB_DIR)/token

# Browser VS Code on http://127.0.0.1:$(CODE_WEB_PORT), loopback only and
# gated by a connection token. Theme lives in the workspace file so the
# desktop VS Code settings for this folder are left alone. Runs the server
# that `code serve-web` downloads directly, because serve-web cannot pass
# --disable-workspace-trust through to it.
code-web:
	@mkdir -p $(CODE_WEB_DIR)/server-data
	@test -s $(CODE_WEB_TOKEN) || (umask 077 && openssl rand -hex 24 > $(CODE_WEB_TOKEN))
	@test -f $(CODE_WEB_WORKSPACE) || printf '%s\n' \
		'{' \
		'  "folders": [{ "path": ".." }],' \
		'  "settings": {' \
		'    "workbench.colorTheme": "Default Dark Modern",' \
		'    "workbench.iconTheme": "vs-seti",' \
		'    "window.commandCenter": true,' \
		'    "editor.fontSize": 14,' \
		'    "editor.minimap.enabled": false,' \
		'    "editor.bracketPairColorization.enabled": true,' \
		'    "editor.guides.bracketPairs": "active",' \
		'    "editor.smoothScrolling": true,' \
		'    "editor.cursorSmoothCaretAnimation": "on",' \
		'    "terminal.integrated.smoothScrolling": true,' \
		'    "workbench.startupEditor": "none",' \
		'    "workbench.tips.enabled": false' \
		'  }' \
		'}' > $(CODE_WEB_WORKSPACE)
	@echo "VS Code web: http://127.0.0.1:$(CODE_WEB_PORT)/?tkn=$$(cat $(CODE_WEB_TOKEN))"
	@(sleep 3 && open "http://127.0.0.1:$(CODE_WEB_PORT)/?tkn=$$(cat $(CODE_WEB_TOKEN))") &
	@server=$$(ls -td $(HOME)/.vscode/cli/serve-web/*/ 2>/dev/null | head -1); \
	if [ -x "$${server}bin/code-server" ]; then \
		exec "$${server}bin/code-server" \
			--host 127.0.0.1 \
			--port $(CODE_WEB_PORT) \
			--connection-token-file $(CODE_WEB_TOKEN) \
			--default-workspace $(CODE_WEB_WORKSPACE) \
			--server-data-dir $(CODE_WEB_DIR)/server-data \
			--accept-server-license-terms \
			--telemetry-level off \
			--disable-workspace-trust; \
	else \
		echo "First run: downloading the VS Code server. Rerun make code-web afterwards to skip the trust prompt."; \
		exec code serve-web \
			--host 127.0.0.1 \
			--port $(CODE_WEB_PORT) \
			--connection-token-file $(CODE_WEB_TOKEN) \
			--default-workspace $(CODE_WEB_WORKSPACE) \
			--server-data-dir $(CODE_WEB_DIR)/server-data \
			--accept-server-license-terms \
			--disable-telemetry; \
	fi
