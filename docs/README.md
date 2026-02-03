# getSecrets Documentation

This directory contains the Sphinx documentation for the getSecrets package.

## Building the Documentation Locally

### Prerequisites

Install the required packages:

```bash
pip install -r requirements.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The generated HTML documentation will be available at `docs/build/html/index.html`.

### Build PDF Documentation

```bash
make latexpdf
```

### Clean Build Files

```bash
make clean
```

## Documentation Structure

- `source/` - Documentation source files (reStructuredText)
    - `conf.py` - Sphinx configuration
    - `index.rst` - Documentation home page
    - `installation.rst` - Installation guide
    - `examples.rst` - Usage examples
    - `api.rst` - API reference
    - `_static/` - Static files (CSS, images)
    - `_templates/` - Custom templates

## ReadTheDocs

This documentation is configured for ReadTheDocs hosting. The configuration is in `.readthedocs.yaml` at the project
root.

To host on ReadTheDocs:

1. Connect your repository to ReadTheDocs
2. The documentation will be automatically built from the `docs/` directory
3. Available formats: HTML, PDF, ePub

## Theme

The documentation uses the Sphinx RTD Theme (Read the Docs theme), which provides a clean, professional look consistent
with ReadTheDocs styling.
