VERSION := $(shell cat VERSION)
PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
SLATE ?= ../slate
# mike runs `mkdocs` from PATH.
export PATH := $(abspath $(BIN)):$(PATH)

.PHONY: help setup serve build reference versions publish capture

help:
	@echo "make setup       create .venv with MkDocs Material and mike"
	@echo "make serve       live preview at http://127.0.0.1:8000"
	@echo "make build       strict build into site/ (fails on broken links)"
	@echo "make reference   copy reference docs from $(SLATE)"
	@echo "make versions    preview the versioned site (gh-pages) at :8000"
	@echo "make publish     deploy $(VERSION) to gh-pages and push (CI does this)"
	@echo "make capture     re-record every GIF (needs DATA=~/tst)"

$(BIN)/mkdocs: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install -q -r requirements.txt
	touch $@

setup: $(BIN)/mkdocs

serve: setup
	$(BIN)/mkdocs serve

build: setup
	$(BIN)/mkdocs build --strict

reference:
	$(PYTHON) scripts/sync_reference.py --slate $(SLATE)

versions: setup
	$(BIN)/mike serve

publish: setup
	$(BIN)/mike deploy --push --update-aliases $(VERSION) latest
	$(BIN)/mike set-default --push $(VERSION)

capture:
	@test -n "$(DATA)" || { echo "set DATA=<demo data dir>, e.g. DATA=~/tst"; exit 1; }
	$(PYTHON) scripts/capture.py --slate $(SLATE) --data $(DATA)
