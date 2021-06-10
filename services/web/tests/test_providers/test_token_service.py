from providers.token_service import TokenService
import pytest
from schema.token_info import GenericTokenInfo


@pytest.fixture
def test_get_all_tokens() -> list[GenericTokenInfo]:
    pass
    # token_service = injector.get(TokenService)
    # return token_service.get_all_tokens()


def test_get_token_info() -> None:
    pass
    # token_service = injector.get(TokenService)
    # token_info = token_service.get_token_info("gZIL")
    # assert token_info.address_bech32 == "zil14pzuzq6v6pmmmrfjhczywguu0e97djepxt8g3e"


def test_token_lookup(test_get_all_tokens: list[GenericTokenInfo]) -> None:
    pass
    # token_service = injector.get(TokenService)
    # token_info = token_service.get_token_info("gZIL")
    # for token in test_get_all_tokens:
    #    if token.address_bech32 == token_info.address_bech32:
    #        assert True
    # assert False
