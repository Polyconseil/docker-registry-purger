.PHONY: update docs quality tests clean

update:
	pip install -r requirements-dev.txt
	pip install -e .

quality:
	python setup.py check --strict --metadata --restructuredtext
	check-manifest
	flake8 src tests setup.py

clean:
	find src "(" -name '*.so' -or -name '*.egg' -or -name '*.pyc' -or -name '*.pyo' ")" -delete
	find src -type d -name __pycache__ -exec rm -r {} \;
	rm -rf .tox .cache build dist
