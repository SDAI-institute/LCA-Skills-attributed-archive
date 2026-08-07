.PHONY: validate validate-strict links test build source validate-dist qualify compile check release-check new-study example claims hashes clean-dist

validate:
	python scripts/validate_repo.py

validate-strict:
	python scripts/validate_repo.py --strict

links:
	python scripts/check_markdown_links.py

test:
	python -m unittest discover -s tests -p 'test_*.py' -v

build:
	python scripts/build_distributions.py --clean

source:
	python scripts/build_source_release.py

validate-dist:
	python scripts/validate_distributions.py

qualify:
	python scripts/host_qualification.py --output dist/reports/host-qualification.json

compile:
	python -m compileall -q lca_tools scripts tests

check: validate-strict links test

release-check: validate-strict links test build source validate-dist qualify compile

new-study:
	python scripts/new_study.py $(SLUG) --title "$(TITLE)"

example:
	python scripts/validate_study.py examples/synthetic-hydrogen-screening --strict
	python scripts/check_balance.py examples/synthetic-hydrogen-screening/balances.csv
	python scripts/run_reference_lca.py --json

claims:
	python scripts/check_claims.py $(STUDY)

hashes:
	python scripts/hash_manifest.py $(STUDY) --update-release

clean-dist:
	rm -rf dist/build dist/packages dist/reports
