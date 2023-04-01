

# test that it imports!
def test_gpt_api_init():
    from gpt_kit.api.core import _GptApi
    api = _GptApi(auto_discover_api_key=False)
    assert api is not None

    from gpt_kit.api.gpt_api import GptApi
    api = GptApi(auto_discover_api_key=False)
    assert api is not None


