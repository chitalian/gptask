import click
import os
from gptask.conf import setup, load_prompts
from gptask.git_checker import is_staged
from gptask.openai_gptask import run



@click.command()
@click.option('-p', '--prompt', help='Prompts in ~/.gptask/prompts')
@click.option('-f', '--force', help='Bypass checking git status', type=bool, default=False)
@click.argument('file', type=click.File('r'))
def main(prompt, force, file):
    setup()
    
    if force == False and is_staged(file.name):
        click.echo(f"File {file.name} has staged changes. Please unstage the file before running gptask.")
        return


    file_contents = file.read()

    all_prompts = load_prompts()

    if prompt not in all_prompts:
        click.echo(f"Prompt {prompt} not found")
        return
    
    if(".gptask" in prompt):
        prompt_contents = all_prompts[prompt[:-7]]
    else:
        prompt_contents = all_prompts[prompt]

    res = run(prompt_contents, file.name, file_contents)
    with open(file.name, 'w') as f:
        f.write(res)


if __name__ == '__main__':
    main()