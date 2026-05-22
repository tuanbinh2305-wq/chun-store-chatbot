"""
Script chạy 1 lần để cấu hình Facebook Messenger:
1. Kiểm tra token hợp lệ
2. Subscribe webhook vào Page (nhận tin nhắn)
3. Cài đặt Get Started button
4. Cài đặt Persistent Menu

Chạy: python setup_messenger.py
"""

import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

PAGE_ID    = os.getenv("FB_PAGE_ID")
TOKEN      = os.getenv("FB_PAGE_ACCESS_TOKEN")
APP_ID     = os.getenv("FB_APP_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")
API_VER    = "v19.0"
BASE       = f"https://graph.facebook.com/{API_VER}"


def check_token() -> bool:
    """Kiểm tra token và quyền hạn."""
    print("\n🔍 Kiểm tra token...")
    resp = requests.get(f"{BASE}/me", params={"access_token": TOKEN, "fields": "name,id"})
    data = resp.json()
    if "name" in data:
        print(f"   ✅ Token hợp lệ — Trang: {data['name']} (ID: {data['id']})")
        return True
    err = data.get("error", {}).get("message", "Lỗi không xác định")
    print(f"   ❌ Token lỗi: {err}")
    return False


def subscribe_page() -> bool:
    """
    Subscribe Page vào app để nhận Messenger events.
    Cần quyền pages_messaging trên token.
    """
    print("\n📡 Subscribe webhook vào Page...")
    resp = requests.post(
        f"{BASE}/{PAGE_ID}/subscribed_apps",
        params={"access_token": TOKEN},
        json={"subscribed_fields": ["messages", "messaging_postbacks", "messaging_optins"]},
    )
    data = resp.json()
    if data.get("success"):
        print("   ✅ Subscribe thành công!")
        return True
    err = data.get("error", {}).get("message", str(data))
    print(f"   ❌ Subscribe thất bại: {err}")
    print("   ℹ️  Cần thêm quyền 'pages_messaging' vào token.")
    print("      Làm theo hướng dẫn trong README.md > Bước 3")
    return False


def set_get_started() -> bool:
    """Cài nút 'Bắt đầu' khi KH mở Messenger lần đầu."""
    print("\n🚀 Cài đặt Get Started button...")
    resp = requests.post(
        f"{BASE}/me/messenger_profile",
        params={"access_token": TOKEN},
        json={"get_started": {"payload": "GET_STARTED"}},
    )
    data = resp.json()
    if data.get("result") == "Successfully updated messenger profile properties":
        print("   ✅ Get Started button đã được cài!")
        return True
    print(f"   ⚠️  {data}")
    return False


def set_persistent_menu() -> bool:
    """Cài menu cố định trong Messenger."""
    print("\n📋 Cài đặt Persistent Menu...")
    menu = {
        "persistent_menu": [{
            "locale": "default",
            "composer_input_disabled": False,
            "call_to_actions": [
                {
                    "type": "postback",
                    "title": "💰 Bảng giá sản phẩm",
                    "payload": "QR_💰 BẢNG GIÁ",
                },
                {
                    "type": "postback",
                    "title": "🎁 Xem combo tiết kiệm",
                    "payload": "QR_🎁 XEM COMBO",
                },
                {
                    "type": "postback",
                    "title": "🚚 Thông tin giao hàng",
                    "payload": "QR_🚚 THÔNG TIN SHIP",
                },
                {
                    "type": "postback",
                    "title": "🛒 Đặt hàng ngay",
                    "payload": "QR_🛒 ĐẶT HÀNG NGAY",
                },
                {
                    "type": "postback",
                    "title": "🔄 Đổi trả / Chính sách",
                    "payload": "QR_🔄 ĐỔI TRẢ",
                },
            ],
        }]
    }
    resp = requests.post(
        f"{BASE}/me/messenger_profile",
        params={"access_token": TOKEN},
        json=menu,
    )
    data = resp.json()
    if data.get("result") == "Successfully updated messenger profile properties":
        print("   ✅ Persistent Menu đã được cài!")
        return True
    print(f"   ⚠️  {data}")
    return False


def set_greeting() -> bool:
    """Cài lời chào hiển thị trước khi KH gõ tin nhắn."""
    print("\n👋 Cài đặt lời chào...")
    resp = requests.post(
        f"{BASE}/me/messenger_profile",
        params={"access_token": TOKEN},
        json={
            "greeting": [
                {
                    "locale": "default",
                    "text": "Chào {{user_first_name}}! 🏠 Chun Store — đồ gia dụng Hàn Quốc giúp bếp gọn đẹp. Nhắn tin để em tư vấn nhé!",
                }
            ]
        },
    )
    data = resp.json()
    if data.get("result") == "Successfully updated messenger profile properties":
        print("   ✅ Lời chào đã được cài!")
        return True
    print(f"   ⚠️  {data}")
    return False


if __name__ == "__main__":
    import sys as _sys
    if hasattr(_sys.stdout, 'reconfigure'):
        _sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    print("=" * 50)
    print("  CHUN STORE CHATBOT — SETUP MESSENGER")
    print("=" * 50)

    if not PAGE_ID or not TOKEN:
        print("❌ Thiếu FB_PAGE_ID hoặc FB_PAGE_ACCESS_TOKEN trong .env")
        sys.exit(1)

    ok = check_token()
    if not ok:
        print("\n❌ Token không hợp lệ. Kiểm tra lại .env")
        sys.exit(1)

    subscribe_page()
    set_get_started()
    set_greeting()
    set_persistent_menu()

    print("\n" + "=" * 50)
    print("✅ Setup hoàn tất!")
    print("\nBước tiếp theo:")
    print("1. Chạy webhook: python webhook.py")
    print("2. Expose qua ngrok: ngrok http 5000")
    print("3. Dán URL vào FB Developer > Messenger > Webhooks")
    print("=" * 50)
