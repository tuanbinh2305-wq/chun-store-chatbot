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
import sys
from dotenv import load_dotenv
from pathlib import Path

from scenarios import find_scenario
from conversation_db import save_message, get_history
from business_context import get_system_prompt
import messenger

load_dotenv(Path(__file__).parent.parent / ".env")

_client = None


def _get_client():
    global _client
    if _client is None:
        import anthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY chưa được cấu hình")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


def _ask_claude(sender_id: str, user_message: str) -> str:
    history = get_history(sender_id)

    # Chuyển history sang format Claude
    messages = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    # Thêm tin nhắn hiện tại
    messages.append({"role": "user", "content": user_message})

    try:
        client = _get_client()
        resp = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=512,
            system=get_system_prompt(),
            messages=messages,
        )
        return resp.content[0].text.strip()
    except Exception as e:
        print(f"[bot_logic] Claude lỗi: {type(e).__name__}: {e}", flush=True)
        sys.stderr.write(f"[bot_logic] Claude lỗi: {type(e).__name__}: {e}\n")
        sys.stderr.flush()
        # Fallback hữu ích thay vì "sự cố kỹ thuật" vô nghĩa
        return (
            "Chị ơi, em chưa hiểu ý chị lắm. Chị thử chọn nha:\n\n"
            "- Xem giá: gõ \"giá\"\n"
            "- Xem combo tiết kiệm: gõ \"combo\"\n"
            "- Đặt hàng: gõ \"đặt hàng\"\n"
            "- Gọi tư vấn: Zalo 0xxx.xxx.xxx\n\n"
            "Hoặc chị cứ hỏi lại, em sẽ trả lời nha!"
        )


def handle_message(sender_id: str, message_text: str) -> None:
    if not message_text or not message_text.strip():
        return

    text = message_text.strip()

    messenger.mark_seen(sender_id)
    messenger.send_typing_on(sender_id)

    save_message(sender_id, "user", text)

    scenario = find_scenario(text)

    if scenario:
        reply = scenario.response
        save_message(sender_id, "assistant", reply)
        messenger.send_typing_off(sender_id)

        if scenario.quick_replies:
            messenger.send_quick_replies(sender_id, reply, scenario.quick_replies)
        else:
            messenger.send_text(sender_id, reply)

    else:
        reply = _ask_claude(sender_id, text)
        save_message(sender_id, "assistant", reply)
        messenger.send_typing_off(sender_id)

        # Nếu AI lỗi (fallback message), gửi kèm quick replies để KH bấm
        if "chị thử chọn nha" in reply:
            messenger.send_quick_replies(
                sender_id, reply,
                ["Xem giá", "Xem combo", "Đặt hàng", "Tư vấn thêm"],
            )
        else:
            messenger.send_text(sender_id, reply)


def handle_postback(sender_id: str, payload: str) -> None:
    payload_map = {
        "GET_STARTED": "chào",
        # Quick replies mới (không emoji)
        "QR_Xem bảng giá": "giá bao nhiêu",
        "QR_Xem giá": "giá bao nhiêu",
        "QR_Xem combo": "combo",
        "QR_Tư vấn thêm": "tư vấn",
        "QR_Thông tin ship": "ship",
        "QR_Đặt hàng": "đặt hàng",
        "QR_Đặt hàng ngay": "đặt hàng",
        "QR_Đặt combo ngay": "muốn mua combo",
        "QR_Đặt combo tặng": "muốn mua combo",
        "QR_Muốn mua combo": "muốn mua combo",
        "QR_Muốn mua khay tủ lạnh": "muốn mua khay tủ lạnh",
        "QR_Muốn mua kệ dán tường": "muốn mua kệ dán tường",
        "QR_Xem bảng giá lẻ": "giá bao nhiêu",
        "QR_Xem combo tiết kiệm": "combo",
        "QR_Xem combo tiết kiệm hơn": "combo",
        "QR_Xem combo tặng": "combo",
        "QR_Xem combo freeship": "combo",
        "QR_Xem review KH": "review",
        "QR_Xem thêm review": "review",
        "QR_Xem review": "review",
        "QR_Xem hình": "hình",
        "QR_Xem hình thực tế": "hình",
        "QR_Xem hình before/after": "hình",
        "QR_Phí ship bao nhiêu": "ship",
        "QR_Xem giá kệ dán": "muốn mua kệ dán tường",
        "QR_Xem khay 89K": "muốn mua khay tủ lạnh",
        "QR_Xem kệ 129K": "muốn mua kệ dán tường",
        "QR_Xem size": "kích thước",
        "QR_Đặt hàng COD": "đặt hàng",
        "QR_Chính sách đổi trả": "đổi trả",
        "QR_Liên hệ hotline": "hotline",
        "QR_Hỏi thêm": "tư vấn",
        "QR_Lo về giá": "đắt quá",
        "QR_Lo về chất lượng": "chất liệu",
        "QR_Chưa biết chọn gì": "tư vấn",
        # Quick replies cũ (có emoji) — giữ lại tương thích
        "QR_📋 XEM BẢNG GIÁ": "giá bao nhiêu",
        "QR_🛍️ XEM COMBO": "combo",
        "QR_❓ TƯ VẤN THÊM": "tư vấn",
        "QR_🚚 THÔNG TIN SHIP": "ship",
        "QR_🛒 ĐẶT HÀNG NGAY": "đặt hàng",
        "QR_🎁 MUỐN MUA COMBO": "muốn mua combo",
        "QR_🧊 MUỐN MUA KHAY TỦ LẠNH": "muốn mua khay tủ lạnh",
        "QR_🔩 MUỐN MUA KỆ DÁN TƯỜNG": "muốn mua kệ dán tường",
    }
    message = payload_map.get(payload, payload.replace("QR_", "").lower())
    handle_message(sender_id, message)
