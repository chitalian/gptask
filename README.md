# Quick start

Just run the following commands

```bash
python3 -m pip install gptask-cli

gptask -p doc-reviewer README.md
gptask -f -p doc-reviewer -r "docs/use-cases/**/*.mdx"
```

Run locally...

```bash
poetry build
poetry install
python3 -m pip install --force-reinstall dist/gptask_cli-0.1.0-py3-none-any.whl
```
