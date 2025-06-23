"""
torrentbotx 包初始化
提供对外统一接口
"""

# 导入核心功能类
from torrentbotx.config.config import Config
from torrentbotx.core.manager import CoreManager
from torrentbotx.tasks.scheduler import TaskScheduler
from torrentbotx.downloaders.base import get_downloader_instance
from torrentbotx.enums.downloader_type import DownloaderType

__all__ = [
    "Config",
    "CoreManager",
    "TaskScheduler",
    "get_downloader_instance",
    "DownloaderType"
]

"""
使用示例:
from torrentbotx import CoreManager, Config

config = Config()
core = CoreManager(config)
core.start()
"""