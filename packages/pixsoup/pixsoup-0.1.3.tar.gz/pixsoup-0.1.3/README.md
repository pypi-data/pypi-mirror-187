
# The CLI to PixSoup service

[PixSoup](https://pixsoup.com) provides a simple interface to a cloud GPU where you can fine-tune
StableDiffusion using Dreambooth.

For integration with your own tooling check GraphQL [schema](schema.graphql).

## Install

```bash
$ pip install pixsoup
```

## Usage

```bash
$ pixsoup --help
```

## Build

```bash
$ pip install build
$ python -m build
```

#### Publish to PyPI

```bash
$ pip install twine

# test
$ twine upload --verbose -r testpypi dist/*

# live
$ twine upload --verbose dist/*
```

