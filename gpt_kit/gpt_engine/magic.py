"""
Run the gpt commands using default unlimited Engine
"""

from gpt_engine import GptEngine

engine = GptEngine()
def run(prompt, template=None, **kwargs):
    return engine.run(prompt, template, **kwargs)

async def arun(prompt, template=None, **kwargs):
    return await engine.arun(prompt, template, **kwargs)
