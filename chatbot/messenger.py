"""
Gửi tin nhắn về Facebook Messenger qua Graph API.
"""

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

PAGE_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
API_VER    = "v19.0"
BASE_URL   = f"https://graph.facebook.com/{API_VER}/me/messages"


def _post(payload: dict) -> bool:
    """Gọi FB Messenger API. Trả về True nếu thành công."""
    try:
        resp = requests.post(
            BASE_URL,
            params={"access_token": PAGE_TOKEN},
            json=payload,
            timeout=10,
        )
        if resp.status_code == 200:
            return True
        print(f"[messenger] Lỗi API: {resp.status_code} — {resp.text[:200]}")
        return False
    except Exception as e:
        print(f"[messenger] Lỗi kết nối: {e}")
        return False


def send_text(recipient_id: str, text: str) -> bool:
    """Gửi tin nhắn text thuần."""
    return _post({
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE",
    })


def send_quick_replies(recipient_id: str, text: str, replies: list[str]) -> bool:
    """
    Gửi tin nhắn kèm quick reply buttons.
    replies: danh sách chuỗi, tối đa 13 items, mỗi title ≤ 20 ký tự.
    """
    quick_reply_items = [
        {"content_type": "text", "title": r[:20], "payload": f"QR_{r[:20].upper()}"}
        for r in replies[:13]
    ]
    return _post({
        "recipient": {"id": recipient_id},
        "message": {
            "text": text,
            "quick_replies": quick_reply_items,
        },
        "messaging_type": "RESPONSE",
    })


def send_typing_on(recipient_id: str) -> None:
    """Hiển thị icon đang gõ (UX thân thiện hơn)."""
    _post({
        "recipient": {"id": recipient_id},
        "sender_action": "typing_on",
    })


def send_typing_off(recipient_id: str) -> None:
    """Tắt icon đang gõ."""
    _post({
        "recipient": {"id": recipient_id},
        "sender_action": "typing_off",
    })


def mark_seen(recipient_id: str) -> None:
    """Đánh dấu đã đọc tin nhắn."""
    _post({
        "recipient": {"id": recipient_id},
        "sender_action": "mark_seen",
    })
