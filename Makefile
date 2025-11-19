PYTHON ?= python
VENV_DIR ?= .venv
PIP := $(VENV_DIR)/bin/pip
PY := $(VENV_DIR)/bin/python

# Create virtual environment if missing
$(VENV_DIR)/bin/activate:
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate; python -m pip install --upgrade pip

.PHONY: install
install: $(VENV_DIR)/bin/activate
	$(PIP) install -r requirements.txt

.PHONY: run
run: install
	$(PY) run_scrape_suumo.py

.PHONY: run-sample
run-sample: install
	SUUMO_HTML_FILE=$(PWD)/data/sample_suumo.html $(PY) run_scrape_suumo.py

.PHONY: lint
lint:
	$(PYTHON) -m compileall scraper run_scrape_suumo.py

.PHONY: clean
clean:
	rm -rf $(VENV_DIR) data/properties.csv
