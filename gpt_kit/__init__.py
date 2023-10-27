# import toml
# from pathlib import Path

from .api.gpt_api import GptApi

# todo: if only import magic if magic is enabled
# if os.getenv("MAGIC_ENABLED", False):
from .api.magic import gpt_api, complete, complete_chat, edit, insert
from .api.utils import get_token_count, list_models, get_model_limit

# path = Path(__file__).parent.parent / 'pyproject.toml'
# __version__ = toml.load(path)['tool']['poetry']['version']
# del toml, Path, path
from .gpt_engine.gpt_engine import GptEngine
