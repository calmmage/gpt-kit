from .gpt_api import GptApi, DEFAULT_COMPLETE_MODEL, DEFAULT_EDIT_MODEL, \
    DEFAULT_CHAT_MODEL, DEFAULT_INSERT_MODEL

# check if interactive mode?
import os

# if os.getenv("MAGIC_ENABLED", False):
gpt_api = GptApi(auto_discover_api_key=False)


def complete_chat(messages, model=DEFAULT_CHAT_MODEL, max_tokens=None,
                  **kwargs):
    return gpt_api.complete_chat(
        messages=messages,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )


def complete(prompt, model=DEFAULT_COMPLETE_MODEL, max_tokens=None, **kwargs):
    return gpt_api.complete(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )


def edit(prompt, instruction, model=DEFAULT_EDIT_MODEL,
         **kwargs):
    return gpt_api.edit(
        prompt=prompt,
        instruction=instruction,
        model=model,
        **kwargs
    )


def insert(prompt, model=DEFAULT_INSERT_MODEL, max_tokens=None, **kwargs):
    return gpt_api.insert(
        prompt=prompt,
        model=model,
        max_tokens=max_tokens,
        **kwargs
    )
