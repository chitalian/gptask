import click
from gptask.conf import setup, load_prompts
from gptask.openai_gptask import run



@click.command()
@click.option('-p', '--prompt', help='Prompts in ~/.gptask/prompts')
@click.argument('file', type=click.File('r'))
def main(prompt, file):
    setup()

    file_contents = file.read()

    all_prompts = load_prompts()

    if prompt not in all_prompts:
        click.echo(f"Prompt {prompt} not found")
        return
    
    prompt_contents = all_prompts[prompt]



    res = run(prompt_contents, file_contents)


    click.echo(f"Prompt: {prompt}")
    click.echo(f"File: {file}")
    click.echo(f"Response: {res}")



if __name__ == '__main__':
    main()