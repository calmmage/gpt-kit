class GptModels(Enum):
    TEXT_DAVINCI_003 = "text-davinci-003"
    # "text-curie-001"
    TEXT_CURIE_001 = "text-curie-001"

    # "text-davinci-insert-002"
    TEXT_DAVINCI_INSERT_002 = "text-davinci-insert-002"
    # "text-davinci-edit-001"
    TEXT_DAVINCI_EDIT_001 = "text-davinci-edit-001"
    # "code-davinci-edit-001"
    CODE_DAVINCI_EDIT_001 = "code-davinci-edit-001"
    # "code-davinci-002"
    CODE_DAVINCI_002 = "code-davinci-002"


TOKEN_BY_MODEL = {
    GptModels.TEXT_DAVINCI_003: 4000,
    GptModels.TEXT_CURIE_001: 2048,
    # GptModels.TEXT_DAVINCI_INSERT_002: 4000,
    # GptModels.TEXT_DAVINCI_EDIT_001: 4000,
    # GptModels.CODE_DAVINCI_EDIT_001: 4000,
    GptModels.CODE_DAVINCI_002: 8000,
}


def get_token_limit(model="text-davinci-003"):
    # get amount of tokens for each model
    if isinstance(model, Enum):
        # convert to str
        model = model.value
    if isinstance(model, str):
        model = GptModels(model)
    else:
        raise ValueError("model must be a string or GptModels enum")
    return TOKEN_BY_MODEL[model]

# max_response_length = get_token_limit(model) - get_token_count(prompt)
