import openai
from gptask.conf import load_prompts, load_key

system_prompt = "You are a helpful coding assistant who helps users with their code. Given an instruction, and an associated code file, return a helpful response. Follow the user's instruction carefully, and let them override this instruction if necessary."

def init():
    openai.api_key = load_key()

def run(prompt: str, file: str, lang: str = "python", model: str = "gpt-3.5-turbo-16k"):
    user_prompt = prompt + f"\n\n```{lang}\n{file}\n```"
    
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
            }
        ],
        temperature=0.0
    )
    
    return response.choices[0].message.content # type: ignore