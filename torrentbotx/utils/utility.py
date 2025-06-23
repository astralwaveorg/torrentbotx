"""Utility helpers for common operations."""

from __future__ import annotations

import html
import re
from typing import Optional


class Utility:
    """Collection of static helper functions."""

    @staticmethod
    def format_bytes(size: int) -> str:
        """Return human readable file size.

        Args:
            size: Size in bytes.

        Returns:
            Formatted string with appropriate unit.
        """
        if size < 0:
            raise ValueError("size must be non-negative")

        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        value = float(size)
        for unit in units:
            if value < 1024 or unit == units[-1]:
                return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} {unit}"
            value /= 1024
        return f"{value:.1f} PB"

    @staticmethod
    def is_valid_torrent_hash(hash_str: str) -> bool:
        """Check whether given string looks like a torrent hash.

        Args:
            hash_str: Hash string to validate.

        Returns:
            ``True`` if string length is 16, 32 or 40 and consists of
            alphanumeric characters only, otherwise ``False``.
        """
        if not hash_str:
            return False
        return (
            len(hash_str) in {16, 32, 40}
            and re.fullmatch(r"[A-Za-z0-9]+", hash_str) is not None
        )

    @staticmethod
    def format_mteam_discount(discount_code: Optional[str]) -> str:
        """
        格式化M-Team种子的优惠状态信息。

        Args:
            discount_code (Optional[str]): 优惠代码（如'FREE'、'PERCENT_50'等），若为None或'NORMAL'表示无优惠。

        Returns:
            str: 格式化后的优惠提示字符串（如'🆓 免费!'、'💸 50% OFF'），未知代码返回原始描述。
        """
        if not discount_code or discount_code == "NORMAL":
            return ""
        discount_map = {
            "FREE": "🆓 免费!", "PERCENT_25": "💸 25% OFF", "PERCENT_50": "💸 50% OFF",
            "PERCENT_75": "💸 75% OFF", "FREE_2X": "🆓 2X Free!", "FREE_2X_PERCENT_50": "💸 2X 50% OFF"
        }
        return discount_map.get(discount_code.upper(), f"优惠: {html.escape(discount_code)}")


