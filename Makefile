-include Makefile.env
export

.PHONY: $(wildcard *)

## help: show help
help:
	@echo ""
	@echo "Usage:"
	@echo ""
	@sed -n 's/^## //p' Makefile | column -t -s ':' | sed -e 's/^/\t/'
	@echo ""

	ARGS := $(word 2,$(MAKECMDGOALS))
%:
	@:

## setup: setup repository setting
setup:
	@chmod +x ./hooks/rtk_pre_tool_use.py && \
	echo "setup complete!"