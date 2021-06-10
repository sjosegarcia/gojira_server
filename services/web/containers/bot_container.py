from providers.scam_reporter_service import ScamReporterService
from repositories.chat_repository import ChatRepository
from providers.database_service import DatabaseService
from repositories.bot_repository import BotRepository
from providers.token_service import TokenService
from providers.ban_service import BanService
from providers.bot_service import BotService
from providers.cas_service import CasService
from providers.chat_id_service import ChatIdService
from providers.link_removal_service import LinkRemovalService
from providers.welcome_message_service import WelcomeMessageService
from providers.track_chat_service import TrackChatService
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Configuration


class BotContainer(DeclarativeContainer):
    config = Configuration()
    bot_repository = Singleton(BotRepository)
    database_service = Singleton(DatabaseService)
    chat_repository = Singleton(ChatRepository, database_service=database_service)
    bot_service = Singleton(BotService, bot_repository=bot_repository)
    token_service = Singleton(TokenService, bot_repository=bot_repository)
    ban_service = Singleton(
        BanService, bot_repository=bot_repository, chat_repository=chat_repository
    )
    cas_service = Singleton(CasService, bot_repository=bot_repository)
    chatid_service = Singleton(ChatIdService, bot_repository=bot_repository)
    link_removal_service = Singleton(LinkRemovalService, bot_repository=bot_repository)
    welcome_message_service = Singleton(
        WelcomeMessageService, bot_repository=bot_repository
    )
    track_chat_service = Singleton(
        TrackChatService, bot_repository=bot_repository, chat_repository=chat_repository
    )
    # scam_reporter_service = Singleton(
    #    ScamReporterService,
    #    bot_repository=bot_repository,
    #    chat_repository=chat_repository,
    # )
