import pytest

from gpt_kit.api.utils import get_token_count

queries = [
    ("This is a test. Write a fun poem about spinning tops:", 13),
    ("Русский текст. Write a fun poem about spinning tops:", 14),
    ("User1, user2, 6749589, pep, Русский текст. "
     "Write a fun poem about spinning tops:", 27),
    ("Emojis: 🤔, ✅, ??, ??", 13),
    ("Давайте посмотрим, что будет, если мы введем русский текст", 22),
    ("", 0),
    ("12", 1),
    ("a", 1),
    ("user", 1),
    ("1", 1),
    ("ц", 1),
    ("я", 1),
]


@pytest.mark.parametrize("text,real", queries)
def test_get_token_count(text, real):
    token_count = get_token_count(text)
    assert token_count == real

# todo: test parse_model

# todo: test get_model_token_limit
