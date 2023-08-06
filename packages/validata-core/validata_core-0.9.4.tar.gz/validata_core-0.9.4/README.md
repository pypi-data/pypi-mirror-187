# Validata validation core

[![PyPI](https://img.shields.io/pypi/v/validata-core.svg)](https://pypi.python.org/pypi/validata-core)

`validata-core` is a library built over [frictionless-py](https://github.com/frictionlessdata/frictionless-py) which provides tabular data validation with:

- French error messages (see [ERRORS](ERRORS.md))
- Custom checks to handle french specifics (see [CUSTOM CHECKS](validata_core/custom_checks/README.md))

`validata-core` is used by [validata-ui](https://git.opendatafrance.net/validata/validata-ui/) and [validata-api](https://git.opendatafrance.net/validata/validata-api/) as part of the [Validata project](https://validata.fr).

## Try (only for python < 3.10)

Create a virtualenv, run the script against fixtures:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
validata  table.csv --schema /path/to/schema.json --ignore_header_case   
# --ignore_header_case is optional and set to False by default (sensitive to the case by default)
```

A complete list of error messages can found in [ERRORS.md](ERRORS.md)

## Testing

```bash
pip install pytest
pytest --doctest-modules
```

## Release a new version

On master branch :
- Update version in [setup.py](setup.py) and [CHANGELOG.md](CHANGELOG.md) files
- Commit changes using `Release` as commit message
- Create git tag (starting with "v" for the release)
- Git push: `git push && git push --tags`
- Check that pypi package is created ([validata-core pipelines](https://git.opendatafrance.net/validata/validata-core/-/pipelines))


Creating and pushing a new release will trigger the pipeline in order to automatically update validata-core version in its children projects (so far : validata-api and validata-ui) projects.

This pipeline runs when a new tag under the format 'vX.X.X' is pushed. For each project, it will create a new branch in which it updates the `requirements.txt` and the `setup.py` files.

