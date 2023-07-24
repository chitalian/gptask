# GPTask

GPTask is a command-line tool to leverage the power of GPT-4 to automatically format files according to specific prompts.

## Installation

Download the package and install using pip:

```bash
pip install gptask_cli
```

## Usage

The binary of the package is `gptask`. Here are some of the commands:

1. To run the gptask on a specific file:

```bash
gptask -p your_prompt file
```

`your_prompt` should be a prompt stored in `~/.gptask/prompts`.

2. To run the gptask on all _files_ in a directory:

```bash
gptask -p your_prompt example/
# Runs on /example/test.py, /example/test2.js, but NOT /example/sub/test.py
```

3. To run the gptask on a glob pattern, just specify the pattern in file_path:

```bash
gptask -p your_prompt example/*.py
# Runs on /example/test.py but NOT /example/test2.js or /example/sub/test.py
```

4. To run the gptask on all files in a directory recursively:

```bash
gptask -r -p your_prompt example/
# Runs on /example/test.py, /example/test2.js, AND /example/sub/test.py
```

5. To force execution even if some conditions are not met:

```bash
gptask -f -p your_prompt file
```

If a prompt doesn't exist, GPTask will display available prompts.

For example:

```bash
gptask -p non_existent_prompt file
```

This will output:

```
Prompt non_existent_prompt not found
Available prompts:
  prompt1
  prompt2
  ...
```

## Contribution

Contributions are welcomed! Feel free to open an issue or create a pull request.

Running in development:

```bash
rm -rf dist
poetry build
poetry install
python3 -m pip install --force-reinstall dist/gptask_cli-*-py3-none-any.whl
```

Deployment instructions:

```bash
python3 -m pip install homebrew-pypi-poet
python3 -m pip install gptask_cli
poet -f gptask_cli # Copy to ruby file
```

## License

This project is licensed under the MIT License.
