from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

from torrentbotx.bots.telegram.handler import *
from torrentbotx.constant import constant
from torrentbotx.constant.constant import *
from torrentbotx.utils.logger import get_logger

logger = get_logger("telegram_updater")

def setup_application(application: Application, bot_token: str):
    """
    设置机器人应用，注册命令和消息处理器
    """

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.ADD_TASK_BTN}$"), ask_add_mt_id),
            # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.MODIFY_CAT_BTN}$"), ask_setcat_mt_id),
            # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.DELETE_TASK_BTN}$"), ask_del_mt_id),
            MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.SEARCH_TORRENT_BTN}$"), ask_search_keywords),
        ],
        states={
            CHOOSING_ACTION: [
                # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.ADD_TASK_BTN}$"), ask_add_mt_id),
                # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.MODIFY_CAT_BTN}$"), ask_setcat_mt_id),
                # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.DELETE_TASK_BTN}$"), ask_del_mt_id),
                MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.SEARCH_TORRENT_BTN}$"), ask_search_keywords),
            ],
            # ASK_ADD_MT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_add_mt_id)],
            # SELECTING_ADD_CATEGORY: [CallbackQueryHandler(handle_add_category_selection, pattern=f"^{constant.BUTTON_CONFIG.ADD_CAT_PREFIX}")],

            # ASK_SETCAT_MT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_setcat_mt_id)],
            # SELECTING_SETCAT_CATEGORY: [
            #     CallbackQueryHandler(handle_setcat_category_selection, pattern=f"^{constant.BUTTON_CONFIG.MOD_CAT_PREFIX}")],

            # ASK_DEL_MT_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_del_mt_id)],
            # CONFIRM_DEL_OPTIONS: [CallbackQueryHandler(received_del_option, pattern=f"^{constant.BUTTON_CONFIG.DEL_OPT_PREFIX}")],

            ASK_SEARCH_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_search_keywords)],
            SHOWING_SEARCH_RESULTS: [
                # CallbackQueryHandler(handle_search_pagination, pattern=f"^{constant.BUTTON_CONFIG.SEARCH_PAGE_PREFIX}"),
                # CallbackQueryHandler(handle_search_result_selection, pattern=f"^{constant.BUTTON_CONFIG.SEARCH_SELECT_PREFIX}"),
                # CallbackQueryHandler(handle_search_cancel, pattern=f"^{constant.BUTTON_CONFIG.SEARCH_CANCEL_PREFIX}end_search"),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("cancel", cancel),
            CommandHandler("help", help_command),
            # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.CANCEL_BTN}$"), cancel_conversation),
            # MessageHandler(filters.Regex(f"^{constant.BUTTON_CONFIG.CANCEL_OPT}$"), cancel_operation),
            MessageHandler(filters.TEXT, handle_unknown)
        ],
        name="mteam_qb_main_conversation",
        persistent=False,
        allow_reentry=True,
    )

    # application.add_handler(CommandHandler("listcats", list_categories_command))
    # application.add_handler(CommandHandler("qbtasks", qbtasks_command))
    # application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("add", direct_add_torrent_command))

    application.add_handler(conv_handler)

    # application.add_handler(CallbackQueryHandler(qbtasks_page_callback, pattern=f"^{constant.BUTTON_CONFIG.QBTASKS_PAGE_PREFIX}"))

    application.add_handler(MessageHandler(filters.COMMAND, handle_unknown))


    # 其他消息处理
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown))

    # 注册搜索相关处理器
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("search", ask_search_keywords)],
        states={
            ASK_SEARCH_KEYWORDS: [MessageHandler(filters.TEXT & ~filters.COMMAND, received_search_keywords)],
            SHOWING_SEARCH_RESULTS: [CallbackQueryHandler(display_search_results_page, pattern=f"^{constant.BUTTON_CONFIG.SEARCH_PAGE_PREFIX}")]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    ))

async def handle_unknown(update, context):
    """
    处理用户发送的未知消息
    """
    await update.message.reply_text("⚠️ 该命令未定义或无法识别，请使用 /help 获取更多帮助。")
