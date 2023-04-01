import os
from .api.utils import get_token_count
from .api.gpt_api import GptApi

# todo: if only import magic if magic is enabled
# if os.getenv("MAGIC_ENABLED", False):
from .api.magic import gpt_api, complete, complete_chat, edit, insert

