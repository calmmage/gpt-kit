# complate_chat
from gpt_kit import complete_chat

messages = [
    {"role": "user", "content": "Hi! How are you?"},
    {"role": "assistant", "content": "Hi!I'm fine, thanks!"},
    {"role": "user", "content": "Oh, I'm glad to hear that!"},
]
reply = complete_chat(messages, model="gpt-4", max_tokens=100)

# chat
from gpt_kit import chat

chat('Hi! How are you?')
chat("Oh, I'm glad to hear that!")
chat("Help we with this question about Mummies", refresh=True)
