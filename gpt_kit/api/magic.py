from .gpt_api import GptApi

# check if interactive mode?
import os

# if os.getenv("MAGIC_ENABLED", False):
gpt_api = GptApi(auto_discover_api_key=False)


def complete_chat(messages, model='gpt-3.5-turbo', max_tokens=None,
                  **kwargs):
    return gpt_api.complete_chat(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )


def complete(prompt, model='davinci', max_tokens=None, **kwargs):
    return gpt_api.complete(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )


def edit(prompt, instruction, model='davinci', max_tokens=None, **kwargs):
    return gpt_api.edit(
        prompt=prompt,
        instruction=instruction,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )


def insert(prompt, model='davinci', max_tokens=None, **kwargs):
    return gpt_api.insert(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )
