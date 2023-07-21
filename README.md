# GPTask

GPTask is a command-line tool to leverage the power of GPT-4 to automatically format files according to specific prompts.

## Installation

Download the package and install using pip:

```sh
pip install gptask
```

## Usage

The binary of the package is `gptask`. Here are some of the commands:

1. To run the gptask on a specific file:

```sh
gptask -p your_prompt file
```

`your_prompt` should be a prompt stored in `~/.gptask/prompts`.

2. To run the gptask recursively on all files in a directory:

```sh
gptask -r your_directory -p your_prompt
```

3. To force execution even if some conditions are not met:

```sh
gptask -f -p your_prompt file
```

If a prompt doesn't exist, GPTask will display available prompts.

For example:

```sh
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

## License

This project is licensed under the MIT License.
