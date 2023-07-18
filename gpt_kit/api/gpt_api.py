from .core import _GptApi
from .utils import parse_model, get_models, get_token_count, \
    get_model_token_limit

DEFAULT_COMPLETE_MODEL = 'text-davinci-003'
DEFAULT_EDIT_MODEL = 'text-davinci-edit-001'
DEFAULT_INSERT_MODEL = 'text-davinci-003'
DEFAULT_CHAT_MODEL = 'gpt-3.5-turbo'


class GptApi:
    def __init__(self, api_key=None, auto_discover_api_key=True):
        self.api = _GptApi(api_key, auto_discover_api_key)

    @staticmethod
    def parse_results(res, chat=False):
        if chat:
            choices = [choice.message.content for choice in res.choices]
        else:
            choices = [choice.text for choice in res.choices]
        if len(choices) > 1:
            return choices
        else:
            return choices[0]

    def complete(self, prompt, model=DEFAULT_COMPLETE_MODEL, max_tokens=None,
                 **kwargs):
        model = parse_model(model)
        if max_tokens is None:
            max_tokens = self._calculate_max_tokens(prompt, model)
        if model in ['gpt-3.5-turbo', 'gpt-4']:
            messages = [{'content': prompt, 'role': 'user'}]
            res = self.complete_chat(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                **kwargs
            )
            return self.parse_results(res, chat=True)
        res = self.api.complete(
            prompt=prompt, model=model, max_tokens=max_tokens, **kwargs
        )
        return self.parse_results(res)

    def _render_chat_prompt(self, messages):
        return str(messages)

    def complete_chat(self, messages, model=DEFAULT_CHAT_MODEL, max_tokens=None,
                      **kwargs):
        if isinstance(messages, str):
            messages = [{'content': messages, 'role': 'user'}]
        model = self.api.parse_chat_model(model)
        if max_tokens is None:
            prompt = self._render_chat_prompt(messages)
            max_tokens = self._calculate_max_tokens(prompt, model)
        res = self.api.complete_chat(
            messages,
            model=model,
            max_tokens=max_tokens,
            **kwargs
        )
        return self.parse_results(res, chat=True)

    def edit(self, prompt, instruction, model=DEFAULT_EDIT_MODEL, **kwargs):
        model = parse_model(model)
        res = self.api.edit(prompt, instruction, model=model, **kwargs)
        return self.parse_results(res)

    def insert(self, prompt, model, max_tokens=None, **kwargs):
        model = parse_model(model)
        if max_tokens is None:
            max_tokens = self._calculate_max_tokens(prompt, model)
        res = self.api.insert(
            prompt,
            model=model,
            max_tokens=max_tokens,
            **kwargs
        )
        return self.parse_results(res)

    # todo:
    # parse model
    # check token count + max_tokens
    #

    # -----------------
    # extra methods
    # -----------------

    def get_all_models(self):
        # extract names
        models = self.api.get_models()
        return [model.name for model in models]

    def _calculate_max_tokens(self, prompt, model):
        model = parse_model(model)
        token_count = get_token_count(prompt)
        model_token_limit = get_model_token_limit(model)
        return model_token_limit - token_count

    parse_model = staticmethod(parse_model)
    get_models = staticmethod(get_models)
    get_token_count = staticmethod(get_token_count)
    get_model_token_limit = staticmethod(get_model_token_limit)
