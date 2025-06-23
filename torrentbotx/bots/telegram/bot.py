import asyncio

from telegram.ext import Application

from torrentbotx import Config
from torrentbotx.bots.telegram.updater import setup_application
from torrentbotx.core.manager import CoreManager
from torrentbotx.utils.logger import get_logger

logger = get_logger("telegram_bot")


def start_bot(config: Config, core_manager: CoreManager):
    logger.info("🎯 启动 Telegram Bot...")
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    application = Application.builder().token(config.get("TG_BOT_TOKEN_MT")).build()
    application.bot_data.update({
        "core_manager": core_manager,
        "config":  config
    })

    setup_application(application, config.get("TG_BOT_TOKEN_MT"))

    logger.info("🔄 机器人正在运行...")
    application.run_polling()
