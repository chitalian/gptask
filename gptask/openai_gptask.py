import os
import openai
from gptask.conf import load_prompts, load_key

system_prompt = "You are a helpful coding assistant who helps users with their code. Given an instruction, and an associated code file, return a helpful response. Follow the user's instruction carefully, and let them override this instruction if necessary."

def init():
    openai.api_key = load_key()

def run(prompt: str, file_name: str, file: str, model: str = "gpt-3.5-turbo-16k"):
    if ('OPENAI_API_KEY' not in os.environ):
        init()

    user_prompt = f"""Here are the contents of {file_name}
```
{file}
```
Using the contents above please following the following instructions: {prompt}
Please only show me the output, no explanation.
"""
    assistant_helper_prompt = f"""
Sure I will just show you the output with my modified changes to the file without a code block.
"""
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': user_prompt
            },
            {
                'role': 'assistant',
                'content': assistant_helper_prompt
            }
        ],
        temperature=0.0,
    )
    
    return response.choices[0].message.content