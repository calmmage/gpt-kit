import loguru
import openai
from aiolimiter import AsyncLimiter
from dotenv import load_dotenv
from llm_tester.src.prompt_base_classes import TemplatedFullPrompt

from gpt_kit.gpt_engine.config import GptEngineConfig

# rate limiter
rate_limit_per_model = {
    "gpt-4": 200,
    "gpt-3.5-turbo": 3500,
}
rate_limiter_per_model = {
    model: AsyncLimiter(limit, 60) for model, limit in rate_limit_per_model.items()
}


def get_rate_limiter(model):
    # todo: handle fuzzy model names
    return rate_limiter_per_model[model]


class GptEngine:
    def __init__(self, config: GptEngineConfig = None, **kwargs):
        if config is None:
            config = self._load_config(**kwargs)
        self.config = config

        # todo 1: db for logging
        self.logger = self._setup_logger()
        # todo 2: token limit & token count tracking
        #  option 1: overall token limit
        #  option 2: token limit per user
        # todo 3: check / setup openai api
        #  option 1: if api key is present in config
        #  option 2: maybe there's already api key in the env / openai - then not break
        self._setup_openai_api()

    def _load_config(self, **kwargs):
        load_dotenv()
        return GptEngineConfig(**kwargs)

    def _setup_logger(self):
        logger = loguru.logger.bind(app="gpt_engine")
        return logger

    def _setup_openai_api(self):
        config_api_key = self.config.openai_api_key.get_secret_value()
        if config_api_key:
            # warn if openai already has api key
            if getattr(openai, "api_key", None):
                self.logger.warning("OpenAI API key already set, overriding")
            else:
                self.logger.info("Setting OpenAI API key")
            openai.api_key = config_api_key
        else:
            # check if openai has api key
            if not getattr(openai, "api_key", None):
                raise ValueError("OpenAI API key not found")
            else:
                self.logger.warning("No OpenAI API key in config, using existing")

    def run(self, prompt, template=None, user=None, **kwargs):
        if template is None:
            # run with a simple ChatCreate
            self.chat_create(prompt, user=user, **kwargs)
        elif isinstance(template, str):
            # todo: run with a template from a library
            raise NotImplementedError
        elif issubclass(template, TemplatedFullPrompt):  # llm tester prompt template
            raise NotImplementedError

    async def arun(self, prompt, template=None, user=None, **kwargs):
        if template is None:
            # run with a simple ChatCreate
            return await self.achat_create(prompt, user=user, **kwargs)
        elif isinstance(template, str):
            # todo: run with a template from a library
            raise NotImplementedError
        elif issubclass(template, TemplatedFullPrompt):  # llm tester prompt template
            raise NotImplementedError

    def chat_create(self, prompt, **kwargs):
        pass

    async def achat_create(self, prompt, system=None, model=None, **kwargs):
        if system is None:
            system = self.config.default_system_message
        if model is None:
            model = self.config.default_model
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ]
        limiter = get_rate_limiter(model)
        async with limiter:
            response = await openai.ChatCompletion.acreate(
                messages=messages, model=model
            )
        return response.choices[0].message.content

    # todo: add retry in case of error. Or at least handle gracefully
    def run_command(self, command: str, data: str, model=None, **kwargs):
        return self.chat_create(data, system=command, model=model, **kwargs)

    # todo: if reason is length - continue generation
    async def arun_command(self, command: str, data: str, model=None, **kwargs):
        return await self.achat_create(data, system=command, model=model, **kwargs)


if __name__ == "__main__":
    # test init
    engine = GptEngine()
