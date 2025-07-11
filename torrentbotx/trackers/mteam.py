import html
from typing import Dict, Any, Optional

import requests

from torrentbotx.trackers.common import BaseTracker
from torrentbotx.utils import Utility
from torrentbotx.utils.logger import get_logger
from torrentbotx.enums.mt_category_type import MtCategoryType

logger = get_logger("trackers.mteam")


class MTeamTracker(BaseTracker):
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://kp.m-team.cc"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})

    def search_torrents(self, keyword: str, page: int = 1, page_size: int = 5) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/torrent/search"
        params = {
            "mode": 'normal',
            "keyword": keyword,
            "pageNumber": page,
            "pageSize": page_size,
        }
        logger.info(f"M-Team 搜索种子参数: {params}")
        try:
            response = self.session.post(url, json=params, timeout=20)
            response.raise_for_status()
            data = response.json()
            logger.info(f"M-Team 搜索种子结果: {data}")
            if data.get("message", "").upper() != 'SUCCESS' or "data" not in data:
                logger.warning(f"M-Team 搜索种子失败: {data.get('message', '未知错误')}")
                return None
            response_data_field = data.get("data")
            if not isinstance(response_data_field, dict):
                logger.warning(f"⚠️ M-Team API 搜索 '{keyword}' 返回的 'data' 字段格式错误，期望为字典。")
                return {"torrents": [], "total_results": 0, "current_page_api": 1, "total_pages_api": 0,
                        "items_per_page_api": page_size}
            torrents_list_raw = response_data_field.get("data", [])
            if not isinstance(torrents_list_raw, list):
                logger.warning(f"⚠️ M-Team API 搜索 '{keyword}' 返回的 'data.data' 字段格式错误，期望为列表。")
                torrents_list_raw = []
            formatted_torrents = []
            for t in torrents_list_raw:
                if not isinstance(t, dict):
                    logger.warning(f"⚠️ M-Team API 搜索结果中包含非字典类型的种子项: {t}")
                    continue

                title_to_display = t.get("smallDescr") or t.get("name", "未知标题")
                subtitle_text = ""
                if t.get("smallDescr") and t.get("name") != t.get("smallDescr"):
                    subtitle_text = t.get("name", "")

                category_id = str(t.get('category', '0'))
                category_name = MtCategoryType.get_display_name_by_id(category_id)

                display_text = (f"<b>👉 {html.escape(title_to_display)}</b>\n\n"
                                + (
                                    f"  ◉ 📝 种子名称: <i>{html.escape(subtitle_text[:72] + ('...' if len(subtitle_text) > 72 else ''))}</i>\n" if subtitle_text else "") +
                                f"  ◉ 🆔 MT资源ID: <code>{t.get('id', 'N/A')}</code>\n"
                                f"  ◉ 💾 资源大小: {Utility.format_bytes(int(t.get('size', 0)))}\n"
                                f"  ◉ 📂 资源类型: {html.escape(category_name)}\n"
                                f"  ◉ 💰 优惠状态: {Utility.format_mteam_discount(t.get('status', {}).get('discount', ''))}"
                                ).strip()
                formatted_torrents.append(
                    {"id": str(t.get('id')), "name": title_to_display, "display_text": display_text,
                     "api_details": t})
            return {
                "torrents": formatted_torrents,
                "total_results": response_data_field.get("total", 0),
                "current_page_api": response_data_field.get("pageNumber", page),
                "total_pages_api": response_data_field.get("totalPages", 0),
                "items_per_page_api": response_data_field.get("pageSize", page_size)
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"请求 M-Team 搜索种子时出错: {e}")
            return None
        except Exception as e:
            logger.error(f"解析 M-Team 搜索响应时出错: {e}")
            return None

    def get_torrent_details(self, torrent_id: str) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/api/torrent/detail"
        try:
            response = self.session.post(url, data={"id": torrent_id}, timeout=20)
            response.raise_for_status()
            data = response.json()
            if data.get("message", "").upper() != 'SUCCESS' or "data" not in data:
                logger.warning(f"M-Team 获取种子详情失败: {data.get('message', '未知错误')}")
                return None
            return data["data"]
        except requests.exceptions.RequestException as e:
            logger.error(f"请求 M-Team 种子详情时出错: {e}")
            return None
        except Exception as e:
            logger.error(f"解析 M-Team 种子详情时出错: {e}")
            return None

    def get_download_link(self, torrent_id: str) -> Optional[str]:
        url = f"{self.base_url}/api/torrent/genDlToken"
        try:
            response = self.session.post(url, data={"id": torrent_id}, timeout=20)
            response.raise_for_status()
            data = response.json()
            if data.get("message", "").upper() != 'SUCCESS' or "data" not in data or not data["data"]:
                logger.warning(f"M-Team 获取下载链接失败: {data.get('message', '无Token')}")
                return None
            return data["data"]
        except requests.exceptions.RequestException as e:
            logger.error(f"请求 M-Team 获取下载链接时出错: {e}")
            return None
        except Exception as e:
            logger.error(f"解析 M-Team 下载链接时出错: {e}")
            return None


class MTeamManager:
    """简化的 M-Team 管理器, 仅用于单元测试."""

    def __init__(self, api_client=None) -> None:
        self.api_client = api_client

    def get_torrent_details(self, torrent_id: str):
        return self.api_client.get_torrent_details(torrent_id)

    def get_torrent_download_url(self, torrent_id: str):
        result = self.api_client.get_torrent_download_url(torrent_id)
        if isinstance(result, dict) and "data" in result:
            return result["data"]
        return result

    def search_torrents_by_keyword(self, keyword: str):
        return self.api_client.search_torrents_by_keyword(keyword)

    # 兼容测试文件中残留的 `se_` 调用
    def se_(self, *args, **kwargs):  # pragma: no cover - backward compatibility
        return self.search_torrents_by_keyword(*args, **kwargs)


__all__ = ["MTeamTracker", "MTeamManager"]
