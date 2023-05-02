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

ru_pattern = re.compile(r'[а-яА-ЯёЁ]')
en_pattern = re.compile(r'[a-zA-Z ]')
digit_pattern = re.compile(r'[0-9]')
other_pattern = re.compile(r'[^а-яА-ЯёЁa-zA-Z0-9 ]')


def get_token_count_estimate(text):
    """Estimate the number of tokens in a text.
    for precise count: from gpt_api import get_token_count
    or
    import transformers
    tokenizer = transformers.GPT2TokenizerFast.from_pretrained("gpt2")
    return len(tokenizer.encode(text))
    """
    # Precompile the regex patterns

    # Count russian characters
    ru_count = len(ru_pattern.findall(text))
    # print("ru", ru_count)

    # Count english characters
    en_count = len(en_pattern.findall(text))
    # print("en", en_count)

    # Count digits
    digit_count = len(digit_pattern.findall(text))
    # print("digit", digit_count)

    # Count other characters
    other_count = len(other_pattern.findall(text))
    # print("other", other_count)

    # Calculate the total count
    res = math.ceil(1.2 * ru_count) + \
          (en_count + 3) // 4 + \
          (1.5 * digit_count + 1) // 2 + \
          math.ceil(1.5 * other_count)
    return int(res)


estimate_tokens = get_token_count_estimate


def _get_token_count(text):
    # calculate amount of tokens in text
    import transformers
    tokenizer = transformers.GPT2TokenizerFast.from_pretrained("gpt2")
    return len(tokenizer.encode(text))


def get_token_count(text, exact=False):
    if exact:
        return _get_token_count(text)
    else:
        return get_token_count_estimate(text)


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
