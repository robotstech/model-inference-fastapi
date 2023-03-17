# model-inference-fastapi

Running inference on ML model over http using fastapi

## prerequisite

create an `.env` file by using the `.example.env` template/sample and fill in the right details

## Run tests

```shell
pytest
pytest --cov=model_inference_fastapi #with coverage
```

## Build

Pypi [doc](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives)

Clean build

```shell
python3 setup.py clean
rm -rf dist
```

Run build

```shell
python3 -m pip install --upgrade build
python3 -m build
```

## Pre Publish

Pypi [doc](https://packaging.python.org/en/latest/tutorials/packaging-projects/#uploading-the-distribution-archives)

### Set up pypirc for token auth

To create token visit [api-tokens](https://test.pypi.org/manage/account/#api-tokens) in test pypi. To use this API
token:

- Set your username to __token__
- Set your password to the token value, including the pypi- prefix.

For example, if you are using Twine to upload your projects to PyPI, set up your `$HOME/.pypirc` file like this:

```toml
[testpypi]
username = '__token__'
password = 'testpypi token'
```

To publish to TestPypi

```shell
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

To install from TestPypi run

```shell
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps model-inference-fastapi
```

## Publishing

Follow the above instructions but for [pypi](https://pypi.org/) not [testpypi](https://test.pypi.org/)

```shell
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```