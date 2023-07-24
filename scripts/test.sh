#! /bin/bash

rm -rf dist
poetry build
poetry install
python3 -m pip install --force-reinstall dist/gptask_cli-*-py3-none-any.whl