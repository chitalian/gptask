import click
import os
import glob
from gptask_cli.conf import run_reload_example_prompts, setup, load_prompts
from gptask_cli.git_checker import is_staged
from gptask_cli.openai_gptask import run

def check_file_staged_status(file, force):
    if not force and is_staged(file.name):
        click.echo(f"File {file.name} has staged changes. Please unstage the file before running gptask.")
        return False
    return True

def _get_path_list(path: str, is_recursive: bool):
    """
    Returns a list of paths from a glob pattern, file, or directory to recurse through.
    """
    if("*" in path):
        return glob.glob(path, recursive=True)
    elif os.path.isfile(path):
        return [path]
    elif(path[-1] == "/"):
        path = path[:-1]
    
    # Recurse (or don't) through directory
    return glob.glob(path + "/**/*" if is_recursive else path + "/*", recursive=True)

def _get_files_from_paths(path_list: list[str]):
    return [f for f in path_list if os.path.isfile(f)]

def _get_file_list (pattern: str, is_recursive: bool):
    paths = _get_path_list(pattern, is_recursive)
    return _get_files_from_paths(paths)

def _get_file_contents_to_process(pattern: str, is_recursive: bool):
    file_list = _get_file_list(pattern, is_recursive)
    return [open(f, 'r') for f in file_list]

def get_prompt_contents(prompt, all_prompts):
    if(".gptask" in prompt):
        return all_prompts[prompt[:-7]]
    else:
        return all_prompts[prompt]

@click.command()
@click.version_option()
@click.option('-p', '--prompt', help='Prompts in ~/.gptask/prompts')
@click.option('-f', '--force', is_flag=True, help='Force execution even if conditions are not met')
@click.option('-r', '--recursive', is_flag=True, help='If true and pattern is a directory, files will be recursively prompted instead of just the top level')
@click.option('-l', '--print-files', is_flag=True, help='Prints the files to be processed')
@click.option('-a', '--print-prompts', is_flag=True, help='Prints all available prompts')
@click.option('-g', '--reload-example-prompts', is_flag=True, help='Reloads example prompts')
@click.argument('pattern', type=click.STRING, required=True)
def main(prompt, force, print_files, recursive, print_prompts,reload_example_prompts, pattern):

    setup()
    if reload_example_prompts:
        run_reload_example_prompts()
        return
    
    if print_files:
        click.echo("Files to be processed:")
        files_to_print = _get_file_list(pattern, recursive)
        for file in files_to_print:
            click.echo(f"  {file}")
        return

    all_prompts = load_prompts()
    if print_prompts:
        click.echo("Available prompts:")
        all_prompts = load_prompts()
        for key in all_prompts.keys():
            click.echo(f"  {key}")
        return

    files_to_process = _get_file_contents_to_process(pattern, recursive)
    if not files_to_process or len(files_to_process) == 0:
        click.echo(f"No files found for path/pattern/directory: {pattern}")
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
