import asyncio
import html
from typing import Union, Optional, List

import telegram
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from torrentbotx import CoreManager, Config
from torrentbotx.constant.constant import ASK_SEARCH_KEYWORDS, SHOWING_SEARCH_RESULTS, CHOOSING_ACTION, BUTTON_CONFIG
from torrentbotx.trackers import MTeamTracker
from torrentbotx.utils.logger import get_logger
from torrentbotx.constant import constant

logger = get_logger("telegram_handler")


async def get_main_keyboard() -> InlineKeyboardMarkup:
    """生成主菜单键盘布局"""
    buttons = [
        [InlineKeyboardButton(BUTTON_CONFIG["ADD_TASK_BTN"], callback_data="add_task")],
        [InlineKeyboardButton(BUTTON_CONFIG["SEARCH_TORRENT_BTN"], callback_data="search_torrent")],
        [InlineKeyboardButton(BUTTON_CONFIG["DELETE_TASK_BTN"], callback_data="delete_task")],
        [InlineKeyboardButton(BUTTON_CONFIG["MODIFY_CAT_BTN"], callback_data="modify_category")],
        [InlineKeyboardButton(BUTTON_CONFIG["CANCEL_BTN"], callback_data="cancel_operation")]
    ]
    return InlineKeyboardMarkup(buttons)

async def common_input_ask(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str, next_state: int,
                           operation_name: str) -> int:
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(
        f"用户 {user.id if user else 'Unknown'} (Chat {chat_id}) 请求进行 '{operation_name}' 操作。提示用户输入。")
    await update.message.reply_text(prompt, reply_markup=await get_main_keyboard())
    return next_state


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start 命令处理，向用户发送欢迎消息
    """
    user = update.effective_user
    logger.info(f"欢迎用户: {user.id if user else 'Unknown'}")
    await update.message.reply_text(f"您好，{user.mention_html()}！欢迎使用我们的自动化下载工具。", parse_mode="HTML")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help 命令处理，向用户展示帮助信息
    """
    help_text = (
        "<b>💡 M-Team 与 qBittorrent 管理助手 - 帮助信息</b>\n\n"
        "<b>主菜单操作 (通过下方按钮触发):</b>\n"
        f"  <code>{constant.BUTTON_CONFIG.ADD_TASK_BTN}</code>: 根据 M-Team 种子ID 添加下载任务到 qBittorrent。\n"
        f"  <code>{constant.BUTTON_CONFIG.MODIFY_CAT_BTN}</code>: 修改 qBittorrent 中现有任务的分类。\n"
        f"  <code>{constant.BUTTON_CONFIG.SEARCH_TORRENT_BTN}</code>: 通过关键词在 M-Team 网站搜索种子。\n"
        f"  <code>{constant.BUTTON_CONFIG.DELETE_TASK_BTN}</code>: 从 qBittorrent 删除任务 (可选是否删除文件)。\n"
        f"  <code>{constant.BUTTON_CONFIG.CANCEL_BTN}</code>: 取消当前操作并返回主菜单。\n\n"
        f"  <code>{constant.BUTTON_CONFIG.CANCEL_OPT}</code>: 取消当前操。\n\n"
        "<b>快捷命令:</b>\n"
        "  <code>/start</code> - 显示主菜单，开始交互。\n"
        "  <code>/add &lt;M-Team ID&gt;</code> - 直接添加指定 M-Team ID 的种子到 qBittorrent。例如: <code>/add 12345</code>\n"
        "  <code>/cancel</code> - (在操作过程中) 取消当前操作。\n"
        "  <code>/help</code> - 显示此帮助信息。\n"
        "  <code>/listcats</code> - 显示 qBittorrent 中的所有分类及其保存路径。\n"
        "  <code>/qbtasks [页码]</code> - 分页显示 qBittorrent 中的任务列表。例如: <code>/qbtasks 2</code>。\n"
    )
    await update.message.reply_html(help_text, reply_markup=await get_main_keyboard())


async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /add [M-Team ID] 命令处理，添加下载任务
    """
    if not context.args:
        await update.message.reply_text("⚠️ 请输入 M-Team ID，例如: /add 12345")
        return

    mt_id = context.args[0]
    logger.info(f"用户请求添加 M-Team ID {mt_id} 的任务。")
    core_manager = context.bot_data["core_manager"]

    # 执行下载任务
    success = core_manager.execute_task("download", {"torrent_id": mt_id})
    if success:
        await update.message.reply_text(f"✅ 已成功添加种子 ID {mt_id} 到下载队列。")
    else:
        await update.message.reply_text(f"❌ 无法添加种子 ID {mt_id}，请稍后再试。")


async def qbtasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /qbtasks 命令处理，查看当前的下载任务状态
    """
    logger.info("用户请求查看当前下载任务。")
    core_manager = context.bot_data["core_manager"]

    # 获取当前任务列表
    tasks = core_manager.execute_task("get_current_tasks", {})
    if tasks:
        tasks_text = "\n".join([f"📝 {task['name']} - 状态: {task['status']}" for task in tasks])
        await update.message.reply_text(f"🔄 当前下载任务：\n{tasks_text}")
    else:
        await update.message.reply_text("❌ 当前没有任何下载任务。")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /cancel 命令处理，取消当前任务
    """
    logger.info(f"用户请求取消当前任务。")
    core_manager = context.bot_data["core_manager"]

    # 执行取消任务
    success = core_manager.execute_task("cancel_current_task", {})
    if success:
        await update.message.reply_text("✅ 已成功取消当前任务。")
    else:
        await update.message.reply_text("❌ 无法取消任务，可能没有正在进行的任务。")


async def ask_search_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await common_input_ask(update, context, "请输入搜索关键词:", ASK_SEARCH_KEYWORDS, "搜索种子-输入关键词")

async def received_search_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message or not update.message.text: return ASK_SEARCH_KEYWORDS

    keywords = update.message.text.strip()
    if not keywords:
        await update.message.reply_text(
            "⚠️ 搜索关键词不能为空，请输入有效的关键词，或使用 /cancel 取消。",
            reply_markup=await get_main_keyboard()
        )
        return ASK_SEARCH_KEYWORDS

    logger.info(f"用户 {update.effective_user.id} 输入了搜索关键词: '{keywords}'")
    context.user_data.update({'search_keywords': keywords, 'search_mode': "normal"})

    return await display_search_results_page(update, context, page_num=0)

async def display_search_results_page(
        update_obj: Union[Update, telegram.CallbackQuery],
        context: ContextTypes.DEFAULT_TYPE,
        page_num: int
) -> int:
    config: Config = context.bot_data['config']
    core_manager: CoreManager = context.bot_data['core_manager']
    mteam: MTeamTracker = core_manager.get_tracker("mteam")

    chat_id: Optional[int] = None
    message_to_handle: Optional[telegram.Message] = None

    if isinstance(update_obj, Update):
        if update_obj.effective_chat: chat_id = update_obj.effective_chat.id
        message_to_handle = update_obj.message
    elif isinstance(update_obj, telegram.CallbackQuery):
        if update_obj.message and update_obj.message.chat:
            chat_id = update_obj.message.chat.id
            message_to_handle = update_obj.message
        await update_obj.answer()

    if not chat_id or not message_to_handle:
        logger.error("🚫 display_search_results_page: 无法确定 chat_id 或要处理的消息。")
        return ConversationHandler.END

    keywords = context.user_data.get('search_keywords')
    if not keywords:
        logger.error("内部错误：display_search_results_page 中关键词丢失。")
        error_msg = "❌ 内部错误：搜索关键词信息丢失。"
        if isinstance(update_obj, telegram.CallbackQuery):
            await message_to_handle.edit_text(error_msg, reply_markup=None)
        else:
            await message_to_handle.reply_text(error_msg, reply_markup=await get_main_keyboard())
        return ConversationHandler.END

    processing_msg_obj: Optional[telegram.Message] = None
    if isinstance(update_obj, Update):
        processing_msg_obj = await message_to_handle.reply_text(
            f"🔍 正在为 “{html.escape(keywords)}” 搜索 M-Team 种子 (第 {page_num + 1} 页)..."
        )

    results_data = await asyncio.to_thread(
        mteam.search_torrents,
        keyword=keywords,
        page=page_num + 1
    )

    if processing_msg_obj:
        try:
            await processing_msg_obj.delete()
        except Exception:
            pass

    if not results_data:
        error_msg = f"⚠️ 搜索 “{html.escape(keywords)}” 时出错，或 M-Team API 未返回有效数据。请稍后再试。"
        if isinstance(update_obj, telegram.CallbackQuery):
            await message_to_handle.edit_text(error_msg, reply_markup=None)
        else:
            await message_to_handle.reply_text(error_msg, reply_markup=await get_main_keyboard())
        return SHOWING_SEARCH_RESULTS

    context.user_data['last_search_results'] = results_data

    torrents = results_data.get("torrents", [])
    total_results = results_data.get("total_results", 0)
    current_page_api = results_data.get("current_page_api", page_num + 1)
    total_pages_api = 0
    try:
        total_pages_api = int(results_data.get("total_pages_api", 0))
    except ValueError:
        logger.warning(f"M-Team API 返回了无法解析的 totalPages: '{results_data.get('total_pages_api')}'. 默认为0.")

    if not torrents and total_results == 0:
        msg_no_results = f"🤷 未找到与 “{html.escape(keywords)}” 相关的 M-Team 种子。"
        if isinstance(update_obj, telegram.CallbackQuery):
            await message_to_handle.edit_text(msg_no_results, reply_markup=None)
        else:
            await message_to_handle.reply_text(msg_no_results, reply_markup=await get_main_keyboard())
        context.user_data.pop('search_keywords', None)
        context.user_data.pop('last_search_results', None)
        return CHOOSING_ACTION

    header = f"🔎 <b>搜索结果: “{html.escape(keywords)}”</b> (共 {total_results} 个)"
    content_parts = [t['display_text'] for t in torrents]

    keyboard_rows: List[List[InlineKeyboardButton]] = []
    for t in torrents:
        btn_text_name = t['name'][:30] + '...' if len(t['name']) > 30 else t['name']
        keyboard_rows.append([
            InlineKeyboardButton(f"📥 下载: {html.escape(btn_text_name)} (ID: {t['id']})",
                                 callback_data=f"{constant.PREFIXES.SEARCH_SELECT_PREFIX}{t['id']}")
        ])

    pagination_buttons_row: List[InlineKeyboardButton] = []
    if page_num > 0:
        pagination_buttons_row.append(
            InlineKeyboardButton("⬅️ 上一页", callback_data=f"{constant.PREFIXES.SEARCH_PAGE_PREFIX}{page_num - 1}")
        )
    if (page_num + 1) < total_pages_api:
        pagination_buttons_row.append(
            InlineKeyboardButton("➡️ 下一页", callback_data=f"{constant.PREFIXES.SEARCH_PAGE_PREFIX}{page_num + 1}")
        )
    if pagination_buttons_row:
        keyboard_rows.append(pagination_buttons_row)

    keyboard_rows.append(
        [InlineKeyboardButton("❌ 取消搜索并返回主菜单", callback_data=f"{constant.PREFIXES.SEARCH_CANCEL_PREFIX}end_search")])

    page_info_footer = ""
    if total_pages_api > 0:
        page_info_footer = f"\n\n📄 第 <b>{current_page_api} / {total_pages_api}</b> 页"

    separator = "\n" + "─" * 20 + "\n"
    full_text = header + "\n" + separator.join(content_parts) + page_info_footer

    final_reply_markup = InlineKeyboardMarkup(keyboard_rows)

    try:
        if isinstance(update_obj, telegram.CallbackQuery):
            await message_to_handle.edit_text(full_text, parse_mode=ParseMode.HTML, reply_markup=final_reply_markup,
                                              disable_web_page_preview=True)
        else:
            await context.bot.send_message(
                chat_id,
                full_text,
                parse_mode=ParseMode.HTML,
                reply_markup=final_reply_markup,
                disable_web_page_preview=True
            )
    except telegram.error.BadRequest as e:
        if "message is too long" in str(e).lower():
            simplified_text = header + "\n\n搜索结果过多，无法在此完整显示。\n请尝试缩小搜索范围或使用分页按钮。" + page_info_footer
            if isinstance(update_obj, telegram.CallbackQuery):
                await message_to_handle.edit_text(simplified_text, parse_mode=ParseMode.HTML,
                                                  reply_markup=final_reply_markup)
            else:
                await context.bot.send_message(chat_id, simplified_text, parse_mode=ParseMode.HTML,
                                               reply_markup=final_reply_markup)
        elif "message is not modified" not in str(e).lower():
            logger.error(f"编辑/发送搜索结果页时出错: {e}")
            await context.bot.send_message(chat_id, "显示搜索结果时出错，请重试。",
                                           reply_markup=await get_main_keyboard())
            return CHOOSING_ACTION
    except Exception as e:
        logger.error(f"显示搜索结果页时发生未知错误: {e}", exc_info=True)
        await context.bot.send_message(chat_id, "显示搜索结果时发生严重错误。", reply_markup=await get_main_keyboard())
        return CHOOSING_ACTION

    return SHOWING_SEARCH_RESULTS
