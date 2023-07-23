import click
import os
import glob
from gptask_cli.conf import setup, load_prompts
from gptask_cli.git_checker import is_staged
from gptask_cli.openai_gptask import run

def check_file_staged_status(file, force):
    if not force and is_staged(file.name):
        click.echo(f"File {file.name} has staged changes. Please unstage the file before running gptask.")
        return False
    return True

def get_files_to_process(recursive, file):
    if file:
        return [file]
    if recursive:
        return [open(f, 'r') for f in glob.glob(recursive, recursive=True)]
    click.echo("Either a file or directory must be provided.")
    return []

def get_prompt_contents(prompt, all_prompts):
    if(".gptask" in prompt):
        return all_prompts[prompt[:-7]]
    else:
        return all_prompts[prompt]

def _print_files(start_path):
    for root, _, files in os.walk(start_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"File Name: {file_path}")
            with open(file_path, 'r') as f:
                print(f"File Contents:\n{f.read()}\n")

@click.command()
@click.version_option()
@click.option('-p', '--prompt', help='Prompts in ~/.gptask/prompts')
@click.option('-f', '--force', is_flag=True, help='Force execution even if conditions are not met')
@click.option('-r', '--recursive', type=click.STRING, help='Directory with files to be processed')
@click.option('-l', '--print-files', is_flag=True, help='Prints the files to be processed')
@click.option('-a', '--print-prompts', is_flag=True, help='Prints all available prompts')
@click.argument('file', type=click.File('r'), required=False)
def main(prompt, force, print_files, recursive, print_prompts, file):
    setup()
    
    if print_files and recursive:
        _print_files(recursive)
        return

    all_prompts = load_prompts()
    if print_prompts:
        click.echo("Available prompts:")
        all_prompts = load_prompts()
        for key in all_prompts.keys():
            click.echo(f"  {key}")
        return

    files_to_process = get_files_to_process(recursive, file)
    if not files_to_process:
        return

    if not all(check_file_staged_status(f, force) for f in files_to_process):
        return

    click.echo(f"The following files will be processed: {[f.name for f in files_to_process]}")
    if not click.confirm("Do you want to continue?", default=True):
        return

    if prompt not in all_prompts:
        if prompt is not None:
            click.echo(f"Prompt {prompt} not found")
        click.echo("Available prompts:")
        for key in all_prompts.keys():
            click.echo(f"  {key}")
        return

    prompt_contents = get_prompt_contents(prompt, all_prompts)

    for file in files_to_process:
        click.echo(f"Using GPT-4 to format (This may take a while): {file.name}")
        file_contents = file.read()
        res = run(prompt_contents, file.name, file_contents)
        with open(file.name, 'w') as f:
            f.write(res)
        file.close()

if __name__ == '__main__':
    main()
