from pydantic import SecretStr
from pydantic_settings import BaseSettings


# class DatabaseConfig(BaseSettings):
#     conn_str: SecretStr = SecretStr("")
#     name: str = ""
#
#     model_config = {
#         "env_prefix": "DATABASE_",
#         # todo:  "GPT_ENGINE_DATABASE_", ?
#     }


class GptEngineConfig(BaseSettings):
    # database: DatabaseConfig = DatabaseConfig()
    openai_api_key: SecretStr = SecretStr("")
    # todo: add extra GPT_ENGINE_ prefix to all env vars?
    #  will this work? - for database config?
    #  "env_prefix": "GPT_ENGINE_"
    default_model: str = "gpt-3.5-turbo"
    default_system_message: str = "You are a helpful assistant"
