# Host qualification commands

Repository checks:

```bash
python scripts/validate_repo.py --strict
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/build_distributions.py --clean
