import os

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
        key = os.environ['OPENAI_API_KEY']
        
    if len(key) == 0:
        raise Exception('No OpenAI key found')
    
    return key