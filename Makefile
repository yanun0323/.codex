SHELL := /bin/bash

SKILLS_DIR ?= $(CURDIR)/skills
OPENCODE_TARGET ?= $(HOME)/.opencode
CLAUDE_TARGET ?= $(HOME)/.claude
SKILLS_DEST_DIR ?= skills

.PHONY: help sync sync-opencode sync-claude sync-target

help:
	@printf '%s\n' \
		'make sync          # Sync skills to both OpenCode and Claude Code' \
		'make sync-opencode # Sync skills to OpenCode target only' \
		'make sync-claude   # Sync skills to Claude Code target only' \
		'make sync-target TARGET=/path/to/target # Sync skills to a custom target' \
		'make sync SKILLS_DEST_DIR=skils # If target uses /skils instead of /skills'

sync: sync-opencode sync-claude

sync-opencode:
	@$(MAKE) sync-target TARGET="$(OPENCODE_TARGET)"

sync-claude:
	@$(MAKE) sync-target TARGET="$(CLAUDE_TARGET)"

sync-target:
	@set -euo pipefail; \
	if [ ! -d "$(SKILLS_DIR)" ]; then \
		echo "Skills directory not found: $(SKILLS_DIR)" >&2; \
		exit 1; \
	fi; \
	if [ -z "$(TARGET)" ]; then \
		echo "TARGET is required. Example: make sync-target TARGET=\$$HOME/.opencode" >&2; \
		exit 1; \
	fi; \
	for dir in "$(SKILLS_DIR)"/* "$(SKILLS_DIR)"/.[!.]* "$(SKILLS_DIR)"/..?*; do \
		[ -d "$$dir" ] || continue; \
		name="$$(basename "$$dir")"; \
		case "$$name" in \
			command-*) category_dir="commands" ;; \
			*) category_dir="$(SKILLS_DEST_DIR)" ;; \
		esac; \
		dest="$(TARGET)/$$category_dir/$$name"; \
		mkdir -p "$$dest"; \
		rsync -a --delete "$$dir/" "$$dest/"; \
		printf 'Synced %s -> %s\n' "$$name" "$$dest"; \
	done
