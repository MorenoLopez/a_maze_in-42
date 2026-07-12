# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: horarivo <horarivo@student.42antananari    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/07/04 21:44:27 by mandrini          #+#    #+#              #
#    Updated: 2026/07/04 22:38:02 by horarivo         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

PYTHON       = python3
VENV         = .venv
ACTIVATE     = . $(VENV)/bin/activate
MAIN         = a_maze_ing.py
CONFIG       = config.txt
PKG_VERSION  = 1.0.0

MYPY_FLAGS = \
	--warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

.PHONY: install run debug clean lint lint-strict build

install:
	$(PYTHON) -m venv $(VENV)
	$(ACTIVATE) && pip install -r requirements.txt
	$(ACTIVATE) && pip install mlx-*.whl;

run:
	$(ACTIVATE) && python3 $(MAIN) $(CONFIG)

debug:
	$(ACTIVATE) && python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \;
	find . -type d -name ".mypy_cache" -prune -exec rm -rf {} \;
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} \;
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	rm -rf $(VENV)

lint:
	$(ACTIVATE) && flake8 .
	$(ACTIVATE) && mypy . $(MYPY_FLAGS)

lint-strict:
	$(ACTIVATE) && flake8 .
	$(ACTIVATE) && mypy . --strict

build:
	$(ACTIVATE) && python3 -m build
	cp dist/mazegen-$(PKG_VERSION).tar.gz .
	cp dist/mazegen-$(PKG_VERSION)-py3-none-any.whl .
	rm -rf dist/ mazegen.egg-info/