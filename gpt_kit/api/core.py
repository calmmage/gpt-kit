import logging
import openai
import os
from dotenv import load_dotenv
from pathlib import Path

logger = logging.getLogger(__name__)


# todo: implement,  move to utils
def input_with_timeout(prompt, default=None, timeout=10):
    raise NotImplementedError


DEFAULT_API_KEY_PATH = Path('~/.openai_api_key').expanduser()


class _GptApi:
    """A simple GPT API class
    support main methods:
    - chat
    - complete
    - insert
    - edit
    later - add more methods:
    - embeddings
    - models
    """

    def __init__(self, api_key=None, auto_discover_api_key=True):
        if api_key is not None:
            openai.api_key = api_key
        elif not openai.api_key and auto_discover_api_key:
            openai.api_key = self._discover_api_key()
        # todo: make sure openai key is set.. ?

    @staticmethod
    def complete_chat(
            messages, model,
            max_tokens=None,
            temperature=None,
            n=None,
            top_p=None,
            stream=None,
            stop=None,
            # user=None,
            **kwargs
    ):
        # model should be:
        # 'gpt-3.5-turbo',
        # 'gpt-4',
        if model not in ['gpt-3.5-turbo', 'gpt-4']:
            raise ValueError(f"model {model} not supported for chat")
        return openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n,
            top_p=top_p,
            stream=stream,
            stop=stop,
            # user=user,
            **kwargs
        )

    @staticmethod
    def complete(
            prompt, model,
            max_tokens=None,
            temperature=None,
            n=None,
            top_p=None,
            stream=None,
            stop=None,
            # user=None,
            **kwargs
    ):
        # if model not in []:
        #     raise ValueError(f"model {model} not supported for chat")
        return openai.Completion.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            n=n,
            top_p=top_p,
            stream=stream,
            stop=stop,
            # user=user,
            **kwargs
        )

    @staticmethod
    def edit(
            prompt, instruction, model,
            temperature=None,
            n=None,
            top_p=None,
            # user=None,
            **kwargs
    ):
        # model should be:
        # 'code-davinci-edit-001',
        # 'text-davinci-edit-001',
        if model not in ['code-davinci-edit-001', 'text-davinci-edit-001']:
            raise ValueError(
                f"model {model} not supported for edit, should be one of: "
                f"'code-davinci-edit-001', 'text-davinci-edit-001'")
        return openai.Edit.create(
            model=model,  # "text-davinci-edit-001",
            input=prompt,  # "What day of the wek is it?",
            instruction=instruction,  # "Fix the spelling mistakes",
            temperature=temperature,
            n=n,
            top_p=top_p,
            # user=user,
            **kwargs
        )

    INSERT_TOKEN = '[insert]'

    def insert(self, prompt, model, **kwargs):
        # model should be:
        # 'text-davinci-003'
        if model not in ['text-davinci-003', 'code-davinci-002']:
            raise ValueError(f"model {model} not supported for insert")
        # INSERT_TOKEN has to be in the prompt exactly once
        if prompt.count(self.INSERT_TOKEN) != 1:
            raise ValueError(
                f"{self.INSERT_TOKEN} must be in the prompt exactly once")
        prefix, suffix = prompt.split(self.INSERT_TOKEN)
        return self.complete(prefix, suffix=suffix, model=model, **kwargs)

    # -----------------
    # extra methods
    # -----------------

    @staticmethod
    def get_models():
        # return openai.Engine.list()
        return openai.Model.list()

    # embedding
    @staticmethod
    def get_embeddings(text, model):
        return openai.Embedding.list(
            model=model,
            query=text,
        )

    # -----------------
    # utils
    # -----------------

    @staticmethod
    def parse_chat_model(model):
        if model in ['gpt-3.5-turbo', 'gpt-4']:
            return model
        # just 2 options for now: 3.5 and 4
        if '4' in model:
            logger.debug('using gpt-4 model')
            return 'gpt-4'
        elif '3.5' in model:
            logger.debug('using gpt-3.5 model')
            return 'gpt-3.5-turbo'
        raise ValueError(f"model {model} is not supported for chat completion")

    @classmethod
    def _discover_api_key(cls):
        # # 1: if key is already defined, return it
        # if openai.api_key is not None:
        #     return openai.api_key

        # 2: if key is not defined, try to load it from .env file
        load_dotenv()
        if os.getenv("OPENAI_API_KEY") is not None:
            return os.getenv("OPENAI_API_KEY")

        # todo 3: config

        # 4: find on disk
        api_key = cls._discover_api_key_on_disk()
        if api_key:
            return api_key

        if not os.getenv("GPT_API_DEV_MODE"):
            raise ValueError(
                "api_key must be provided"
                " or set GPT_API_DEV_MODE=1 for automatic discovery"
            )

        # 5: request from user
        api_key = cls._request_api_key_from_user()
        if api_key:
            # 6: save to disk
            USER_MESSAGE = "Save your API key to disk? (y/N)"
            if input_with_timeout(USER_MESSAGE, 'n') == 'y':
                cls._save_api_key_to_disk(api_key)
            return api_key
        raise ValueError("api_key not found")

    @staticmethod
    def _discover_api_key_on_disk():
        if DEFAULT_API_KEY_PATH.exists():
            return DEFAULT_API_KEY_PATH.read_text()
        # try other paths
        path_candidates = ['.openai_api_key']
        for path in path_candidates:
            if os.path.exists(path):
                return open(path).read()
        return None

    @staticmethod
    def _request_api_key_from_user():
        USER_MESSAGE = "Please provide your OpenAI API key"
        return input_with_timeout(USER_MESSAGE)

    @staticmethod
    def _save_api_key_to_disk(api_key):
        # request path from user, use default path if timeout
        USER_MESSAGE = f"Please provide path to save your API key to disk. " \
                       f"Default path is {DEFAULT_API_KEY_PATH}"
        path = input_with_timeout(USER_MESSAGE, DEFAULT_API_KEY_PATH)
        path.write_text(api_key)
