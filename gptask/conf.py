import click
import os

def setup():
    base_dir = os.path.expanduser('~/.gptask')
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    prompts_dir = os.path.expanduser('~/.gptask/prompts')
    if not os.path.exists(prompts_dir):
        os.makedirs(prompts_dir)
        
    # Check for key
    key_path = os.path.expanduser('~/.gptask/openai.key')
    if not os.path.exists(key_path):
        # Check if key is in env
        if 'OPENAI_API_KEY' in os.environ and click.confirm('Found OpenAI API key in environment. Would you like to save it to ~/.gptask/openai.key? (Y/n)'):
            with open(key_path, 'w') as f:
                f.write(os.environ['OPENAI_API_KEY'])
        else:
            # Ask user to enter key
            key = click.prompt('Enter your OpenAI API key.', type=str)
            with open(key_path, 'w') as f:
                f.write(key)

def load_prompts():
    prompts = {}
    for filename in os.listdir(os.path.expanduser('~/.gptask/prompts')):
        with open(os.path.expanduser('~/.gptask/prompts/' + filename)) as f:
            prompts[filename] = f.read()
            
    return prompts

def load_key():
    # load from ~/.gptask/openai.key
    with open(os.path.expanduser('~/.gptask/openai.key')) as f:
        key = f.read().strip()
        
    if len(key) == 0:
        raise Exception('No OpenAI key found')
    
    return key