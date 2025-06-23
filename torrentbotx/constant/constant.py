from torrentbotx.trackers import MTeamTracker, CarptTracker

BUTTON_CONFIG = {
    "ADD_TASK_BTN": "📥 添加任务",
    "MODIFY_CAT_BTN": "🔄 修改分类",
    "DELETE_TASK_BTN": "🗑️ 删除任务",
    "SEARCH_TORRENT_BTN": "🔍 搜索种子",
    "SUB_TORRENT_BTN": "👻 订阅剧集",
    "CANCEL_BTN": "↩️ 返回菜单",
    "CANCEL_OPT": "🛑 取消操作"
}
# 前缀常量
PREFIXES = {
    "ADD_CAT_PREFIX": "addcat_",
    "MOD_CAT_PREFIX": "modcat_",
    "DEL_OPT_PREFIX": "delopt_",
    "SEARCH_PAGE_PREFIX": "searchpage_",
    "SEARCH_SELECT_PREFIX": "searchsel_",
    "SEARCH_CANCEL_PREFIX": "searchcancel_",
    "QBTASKS_PAGE_PREFIX": "qbtasks_page_",
}

TRACKERS = {
    "mteam": MTeamTracker,
    "carpt": CarptTracker,
}

CHOOSING_ACTION, ASK_ADD_MT_ID, SELECTING_ADD_CATEGORY, ASK_SETCAT_MT_ID,SELECTING_SETCAT_CATEGORY, ASK_DEL_MT_ID, CONFIRM_DEL_OPTIONS,ASK_SEARCH_KEYWORDS, SHOWING_SEARCH_RESULTS = range(9)