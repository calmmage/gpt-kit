import re
import math


def discover_gpt_api_key():
    from gpt_kit.api.core import _GptApi
    return _GptApi._discover_api_key()


def init_gpt_api_key():
    import openai
    openai.api_key = discover_gpt_api_key()


# ----------------------------
# Token counts
# ----------------------------


def get_token_count(text, model="gpt-3.5-turbo"):
    """
    calculate amount of tokens in text
    model: gpt-3.5-turbo, gpt-4, text-davinci-003, text-curie-001, code-davinci-edit-001, text-davinci-edit-001, code-davinci-002
    """
    import tiktoken
    model = parse_model(model)
    # To get the tokeniser corresponding to a specific model in the OpenAI API:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))


# ----------------------------
# Modles
# ----------------------------

# todo: add codex etc.
MODEL_NAMES = [
    "gpt-3.5-turbo",
    "gpt-4",
    "text-davinci-003",
    "text-curie-001",
    'code-davinci-edit-001',
    'text-davinci-edit-001',
    'code-davinci-002',
]

MODEL_TOKEN_LIMITS = {
    "gpt-3.5-turbo": 4000,
    "gpt-4": 8000,
    "text-davinci-003": 4000,
    "text-curie-001": 2048,
    "code-davinci-edit-001": 4000,
    "text-davinci-edit-001": 4000,
    "code-davinci-002": 8000,
}


def parse_model(model: str):
    if model in MODEL_NAMES:
        return model
    candidates = [m for m in MODEL_NAMES if model in m]
    if len(candidates) == 0:
        raise ValueError(f"Model {model} is not supported")
    elif len(candidates) > 1:
        raise ValueError(f"Model {model} is ambiguous: {candidates}")
    return candidates[0]


def list_models():
    return tuple(MODEL_NAMES)


get_models = list_models


def get_model_token_limit(model):
    model = parse_model(model)
    return MODEL_TOKEN_LIMITS[model]


get_token_limit = get_model_limit = get_model_token_limit
