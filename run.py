from torrentbotx.bots.telegram.bot import start_bot
from torrentbotx.config.config import load_config
from torrentbotx.core.manager import CoreManager
from torrentbotx.db.setup import init_db
from torrentbotx.notifications.telegram_notifier import TelegramNotifier


def main():
    config = load_config()
    init_db()

    notifier = TelegramNotifier(
        bot_token=config.get("TG_BOT_TOKEN"),
        chat_id=config.get("TG_ALLOWED_CHAT_IDS")
    )
    core_manager = CoreManager(config=config, notifier=notifier)
    core_manager.start()

    start_bot(config, core_manager)


if __name__ == "__main__":
    main()
