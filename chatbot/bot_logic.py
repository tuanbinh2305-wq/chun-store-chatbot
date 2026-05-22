"""
Logic chính của chatbot — Hybrid (kịch bản + Gemini AI).

Luồng xử lý:
1. Nhận tin nhắn từ KH
2. Kiểm tra kịch bản cố định (scenarios.py)
   → Khớp → Trả lời kịch bản ngay (nhanh, chính xác)
   → Không khớp → Gọi Gemini AI (thông minh, linh hoạt)
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

_model = None


def _get_model():
    global _model
    if _model is None:
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY chưa được cấu hình")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=get_system_prompt(),
        )
    return _model


def _ask_gemini(sender_id: str, user_message: str) -> str:
    history = get_history(sender_id)

    # Chuyển history sang format Gemini
    gemini_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    try:
        model = _get_model()
        import google.generativeai as genai
        chat = model.start_chat(history=gemini_history)
        resp = chat.send_message(user_message)
        return resp.text.strip()
    except Exception as e:
        print(f"[bot_logic] Gemini lỗi: {type(e).__name__}: {e}", flush=True)
        sys.stderr.write(f"[bot_logic] Gemini lỗi: {type(e).__name__}: {e}\n")
        sys.stderr.flush()
        return (
            "Ôi, em đang gặp chút sự cố kỹ thuật 😅 "
            "Chị nhắn lại sau ít phút hoặc gọi hotline để em hỗ trợ nhé ạ!"
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
        reply = _ask_gemini(sender_id, text)
        save_message(sender_id, "assistant", reply)
        messenger.send_typing_off(sender_id)
        messenger.send_text(sender_id, reply)


def handle_postback(sender_id: str, payload: str) -> None:
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
    message = payload_map.get(payload, payload.replace("QR_", "").lower())
    handle_message(sender_id, message)
