SHELL=/bin/bash

# linux
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8
C_FORCE_ROOT:=1


# Simply by being mentioned as a target,
# this tells make to export all variables to child processes by default.
.EXPORT_ALL_VARIABLES:

# python
PYTHON:=python3.10
#PYTHONOPTIMIZE:=1
#PYTHONIOENCODING:=utf-8
#PYTHONTRACEMALLOC:=1
#PYTHONMALLOC:=default
#PYTHONUTF8:=1
VIRTUAL_ENV=${CURDIR}/venv
PATH:=$(VIRTUAL_ENV)/bin:$(PATH)

.PHONY: venv
.ONESHELL:
venv:
	rm -rf $(VIRTUAL_ENV) && $(PYTHON) -m venv $(VIRTUAL_ENV)
	$(VIRTUAL_ENV)/bin/pip install --upgrade pip wheel setuptools
	$(VIRTUAL_ENV)/bin/pip install --requirement requirements.txt

.ONESHELL:
isort:
	isort --use-parentheses --line-length 80 --multi-line 3 healthcheck
