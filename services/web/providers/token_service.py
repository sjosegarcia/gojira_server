from repositories.bot_repository import BotRepository
from schema.token_info import TokenInfo, GenericTokenInfo
from httpx import get, ReadTimeout
from setup.config import get_settings
from fastapi import HTTPException, status
from telegram.ext import CommandHandler
from telegram import ParseMode


class TokenService:
    def __init__(self, bot_repository: BotRepository) -> None:
        self.bot_repository = bot_repository
        self._process_handlers()

    def get_token_info(self, token: str) -> TokenInfo:
        try:
            response = get(f"{get_settings().zilstream_token_url}/{token}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"There is no data available for the specified token you requested. {response.json()}",
                )
            return TokenInfo(**response.json())
        except ReadTimeout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There is no data available for the specified token you requested.",
            )

    def get_all_tokens(self) -> list[GenericTokenInfo]:
        try:
            response = get(f"{get_settings().zilstream_token_url}")
            if response.status_code == status.HTTP_404_NOT_FOUND:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"There was an error retreiving the list of available token data. {response.json()}",
                )
            data = response.json()
            tokens = [GenericTokenInfo(**token_data) for token_data in data]
            return tokens
        except ReadTimeout:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There was an error retreiving the list of available token data.",
            )

    def _process_handlers(self) -> None:
        tokens = self.get_all_tokens()
        for generic_token in tokens:
            token_info = self.get_token_info(generic_token.symbol)
            self._register_token_command(token_info)

    def _register_token_command(self, token_info: TokenInfo) -> None:
        token_website = (
            f"\n<a href='{token_info.website}'>Website</a>"
            if token_info.website
            else ""
        )
        token_whitepaper = (
            f"\n<a href='{token_info.whitepaper}'>Whitepaper</a>"
            if token_info.whitepaper
            else ""
        )
        token_address = (
            f"\n<a href='https://viewblock.io/zilliqa/address/{token_info.address_bech32}'>{token_info.symbol} contract on viewblock.io</a>"
            if token_info.address_bech32
            else ""
        )
        token_zilstream = f"\n<a href='https://zilstream.com/tokens/{token_info.symbol}'>View {token_info.symbol} on zilstream.com</a>"
        token_price = f"\n<b>{token_info.rate:.2f} ZIL - ${token_info.rate_usd:.2f}</b>"
        token_view_info = f"<b>{token_info.name} ({token_info.symbol})\nScore: {token_info.viewblock_score}/100</b>"

        self.bot_repository.updater.dispatcher.add_handler(
            CommandHandler(
                token_info.symbol.lower(),
                lambda update, context: update.message.reply_text(
                    f"{token_view_info}{token_price}{token_website}{token_whitepaper}{token_address}{token_zilstream}",
                    parse_mode=ParseMode.HTML,
                    quote=False,
                    disable_notification=True,
                    disable_web_page_preview=True,
                    allow_sending_without_reply=True,
                ),
            )
        )
