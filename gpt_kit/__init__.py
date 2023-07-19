import importlib.metadata

from .api.gpt_api import GptApi
# todo: if only import magic if magic is enabled
# if os.getenv("MAGIC_ENABLED", False):
from .api.magic import gpt_api, complete, complete_chat, edit, insert
from .api.utils import get_token_count, list_models, get_model_limit

try:
    __version__ = importlib.metadata.version('gpt_kit')
except:
    import logging

    logging.warning('failed to get version of gpt_kit, traceback:',
                    exc_info=True)
