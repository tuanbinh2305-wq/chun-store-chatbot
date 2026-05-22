"""
Logic chính của chatbot — Hybrid (kịch bản + Claude AI).

Luồng xử lý:
1. Nhận tin nhắn từ KH
2. Kiểm tra kịch bản cố định (scenarios.py)
   → Khớp → Trả lời kịch bản ngay (nhanh, chính xác)
   → Không khớp → Gọi Claude AI (thông minh, linh hoạt)
3. Lưu lịch sử vào DB
4. Gửi reply về Messenger
"""

import os
import anthropic
from dotenv import load_dotenv
from pathlib import Path

from scenarios import find_scenario
from conversation_db import save_message, get_history
from business_context import get_system_prompt
import messenger

load_dotenv(Path(__file__).parent.parent / ".env")

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY chưa được cấu hình trong .env"
            )
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def _ask_claude(sender_id: str, user_message: str) -> str:
    """
    Gọi Claude AI với lịch sử hội thoại và context kinh doanh.
    Trả về reply text.
    """
    history = get_history(sender_id)

    # Thêm tin nhắn hiện tại vào cuối
    messages = history + [{"role": "user", "content": user_message}]

    try:
        client = _get_client()
        resp = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=get_system_prompt(),
            messages=messages,
        )
        return resp.content[0].text.strip()
    except anthropic.APIError as e:
        print(f"[bot_logic] Claude API lỗi: {e}")
        return (
            "Ôi, em đang gặp chút sự cố kỹ thuật 😅 "
            "Chị nhắn lại sau ít phút hoặc gọi hotline để em hỗ trợ nhé ạ!"
        )
    except Exception as e:
        print(f"[bot_logic] Lỗi không xác định: {e}")
        return "Em xin lỗi, có lỗi xảy ra. Chị thử lại sau ít phút nhé ạ!"


def handle_message(sender_id: str, message_text: str) -> None:
    """
    Xử lý 1 tin nhắn đến từ KH.
    - sender_id: FB PSID của người gửi
    - message_text: nội dung tin nhắn
    """
    if not message_text or not message_text.strip():
        return

    text = message_text.strip()

    # ── Hiển thị đang gõ ──
    messenger.mark_seen(sender_id)
    messenger.send_typing_on(sender_id)

    # ── Lưu tin nhắn KH ──
    save_message(sender_id, "user", text)

    # ── Bước 1: Tìm kịch bản cố định ──
    scenario = find_scenario(text)

    if scenario:
        # Kịch bản khớp → trả lời ngay
        reply = scenario.response
        save_message(sender_id, "assistant", reply)
        messenger.send_typing_off(sender_id)

        if scenario.quick_replies:
            messenger.send_quick_replies(sender_id, reply, scenario.quick_replies)
        else:
            messenger.send_text(sender_id, reply)

    else:
        # Không khớp kịch bản → gọi Claude AI
        reply = _ask_claude(sender_id, text)
        save_message(sender_id, "assistant", reply)
        messenger.send_typing_off(sender_id)
        messenger.send_text(sender_id, reply)


def handle_postback(sender_id: str, payload: str) -> None:
    """
    Xử lý khi KH bấm nút quick reply / button.
    payload: string từ button (ví dụ 'QR_XEM BẢNG GIÁ').
    """
    # Map payload → tin nhắn tương đương để xử lý như text thường
    payload_map = {
        "GET_STARTED": "chào",
        "QR_📋 XEM BẢNG GIÁ": "giá bao nhiêu",
        "QR_🛍️ XEM COMBO": "combo",
        "QR_❓ TƯ VẤN THÊM": "tư vấn",
        "QR_🚚 THÔNG TIN SHIP": "ship",
        "QR_🛒 ĐẶT HÀNG NGAY": "đặt hàng",
        "QR_🎁 MUỐN MUA COMBO": "muốn mua combo",
        "QR_🧊 MUỐN MUA KHAY TỦ LẠNH": "muốn mua khay tủ lạnh",
        "QR_🔩 MUỐN MUA KỆ DÁN TƯỜNG": "muốn mua kệ dán tường",
    }
    # Tìm trong map, nếu không có thì dùng payload gốc bỏ prefix QR_
    message = payload_map.get(payload, payload.replace("QR_", "").lower())
    handle_message(sender_id, message)
