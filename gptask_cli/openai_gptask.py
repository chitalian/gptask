import os
import openai
from gptask_cli.conf import load_key

system_prompt = "You are a helpful coding assistant who helps users with their code. Given an instruction, and an associated code file, return a helpful response. Follow the user's instruction carefully, and let them override this instruction if necessary."

def init():
    openai.api_key = load_key()

def run(prompt: str, file_name: str, file: str, model: str = "gpt-4"):
    if ('OPENAI_API_KEY' not in os.environ):
        init()
    seperator = "<------------------------------------>"
    user_prompt = f"""{file}
{seperator}
Using the contents above for {file_name} please following the following instructions: {prompt}
Please only show me the output, no explanation.
"""
    assistant_helper_prompt = f"""
Sure I will just show you the output with my modified changes.
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
    
    res: str= response.choices[0].message.content
    res.replace(seperator, '')
    return res
