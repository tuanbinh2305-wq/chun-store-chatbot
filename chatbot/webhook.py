"""
Flask webhook server — nhận tin nhắn từ Facebook Messenger.

Chạy:
  python webhook.py

Expose ra internet (test local):
  ngrok http 5000
  → Lấy URL dán vào FB Developer > Messenger > Webhooks
"""

import os
import threading
from flask import Flask, request, jsonify, abort
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

import conversation_db
import bot_logic

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "chunstore_webhook_2026")


# ──────────────────────────────────────────────
# WEBHOOK VERIFICATION (GET)
# ──────────────────────────────────────────────

@app.get("/webhook")
def verify_webhook():
    """
    Facebook gọi endpoint này 1 lần khi đăng ký webhook.
    Trả về hub.challenge nếu verify_token đúng.
    """
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print(f"[webhook] ✅ Xác minh thành công!")
        return challenge, 200

    print(f"[webhook] ❌ Xác minh thất bại — token nhận được: {token}")
    abort(403)


# ──────────────────────────────────────────────
# NHẬN TIN NHẮN (POST)
# ──────────────────────────────────────────────

@app.post("/webhook")
def receive_message():
    """
    Nhận event từ Facebook Messenger.
    Trả về 200 OK ngay lập tức, xử lý tin nhắn ở background thread.
    """
    data = request.get_json(silent=True)

    if not data or data.get("object") != "page":
        return jsonify({"status": "ignored"}), 200

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")
            if not sender_id:
                continue

            # Tin nhắn text
            if "message" in event:
                msg = event["message"]
                # Bỏ qua echo (tin nhắn do bot tự gửi)
                if msg.get("is_echo"):
                    continue
                text = msg.get("text", "").strip()
                if text:
                    _process_async(sender_id, "message", text)

            # Postback (bấm nút)
            elif "postback" in event:
                payload = event["postback"].get("payload", "")
                if payload:
                    _process_async(sender_id, "postback", payload)

    # FB yêu cầu trả về 200 trong vòng 20 giây
    return jsonify({"status": "ok"}), 200


def _process_async(sender_id: str, event_type: str, data: str) -> None:
    """Xử lý tin nhắn ở thread riêng để không block webhook response."""
    def _run():
        try:
            if event_type == "message":
                bot_logic.handle_message(sender_id, data)
            elif event_type == "postback":
                bot_logic.handle_postback(sender_id, data)
        except Exception as e:
            print(f"[webhook] Lỗi xử lý {event_type} từ {sender_id}: {e}")

    threading.Thread(target=_run, daemon=True).start()


# ──────────────────────────────────────────────
# HEALTH CHECK
# ──────────────────────────────────────────────

@app.get("/")
def health_check():
    return jsonify({
        "status": "running",
        "service": "Chun Store Chatbot",
        "version": "1.0.0",
    })


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import sys, io
    # Fix encoding Windows terminal
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

    conversation_db.init_db()
    print("[OK] Database initialized")
    print(f"[OK] Verify token: {VERIFY_TOKEN}")
    print("[>>] Chatbot running at http://localhost:5000")

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
