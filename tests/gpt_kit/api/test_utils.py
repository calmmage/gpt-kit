from gpt_kit.api.utils import get_token_count_estimate, _get_token_count
import pytest

queries = [
    ("This is a test. Write a fun poem about spinning tops:", 16, 13),
    ("Русский текст. Write a fun poem about spinning tops:", 28, 24),
    ("User1, user2, 6749589, pep, Русский текст. "
     "Write a fun poem about spinning tops:", 45, 37),
    ("Emojis: 🤔, ✅, ??, ??", 18, 15),
    ("Давайте посмотрим, что будет, если мы введем русский текст", 63, 62),
    ("",  0, 0),
    ("12",  2, 1),
    ("a",  1, 1),
    ("user",  1, 1),
    ("1", 1, 1),
    ("ц", 2, 2),
    ("я", 2, 1),
]
@pytest.mark.parametrize("text,est,real", queries)
def test_get_token_count(text,est,real):
    estimate = get_token_count_estimate(text)
    token_count = _get_token_count(text)
    assert token_count == real
    assert estimate == est
    assert estimate >= token_count

# todo: test parse_model

# todo: test get_model_token_limit
