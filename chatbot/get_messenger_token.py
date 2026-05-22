"""
Tự động lấy Facebook Page Token có quyền pages_messaging.
Chạy: python get_messenger_token.py
"""

import os, sys, json, time, threading, webbrowser, requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_PATH, override=True)

APP_ID     = os.getenv("FB_APP_ID")
APP_SECRET = os.getenv("FB_APP_SECRET")
PAGE_ID    = os.getenv("FB_PAGE_ID")
API_VER    = "v19.0"
REDIRECT   = "http://localhost:8765/callback"

SCOPES = ",".join([
    "pages_show_list",
    "pages_manage_posts",
    "pages_read_engagement",
    "pages_manage_metadata",
    "pages_messaging",
    "pages_messaging_subscriptions",
])

received_code = None
server_done   = threading.Event()


class CallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass  # tắt log

    def do_GET(self):
        global received_code
        parsed = urlparse(self.path)

        if parsed.path == "/callback":
            params = parse_qs(parsed.query)
            code   = params.get("code", [None])[0]
            error  = params.get("error", [None])[0]

            if code:
                received_code = code
                html = b"""<html><body style='font-family:sans-serif;text-align:center;padding:40px'>
                <h2>&#10003; Da nhan quyen thanh cong!</h2>
                <p>Quay lai terminal de hoan tat...</p>
                <script>setTimeout(()=>window.close(),2000)</script>
                </body></html>"""
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html)
            else:
                html = f"""<html><body style='font-family:sans-serif;text-align:center;padding:40px'>
                <h2>&#10007; Loi: {error}</h2>
                <p>Dong tab nay va thu lai.</p>
                </body></html>""".encode()
                self.send_response(400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html)

            server_done.set()

        else:
            self.send_response(404)
            self.end_headers()


def exchange_code(code: str) -> str:
    """Code → Short-lived User Token."""
    r = requests.get(f"https://graph.facebook.com/{API_VER}/oauth/access_token", params={
        "client_id":     APP_ID,
        "client_secret": APP_SECRET,
        "redirect_uri":  REDIRECT,
        "code":          code,
    })
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError(f"Loi exchange code: {data}")
    return data["access_token"]


def to_long_lived(short_token: str) -> str:
    """Short-lived → Long-lived User Token (~60 ngay)."""
    r = requests.get(f"https://graph.facebook.com/{API_VER}/oauth/access_token", params={
        "grant_type":        "fb_exchange_token",
        "client_id":         APP_ID,
        "client_secret":     APP_SECRET,
        "fb_exchange_token": short_token,
    })
    data = r.json()
    if "access_token" not in data:
        raise RuntimeError(f"Loi long-lived: {data}")
    return data["access_token"]


def get_page_token(long_user_token: str) -> str:
    """Long-lived User Token → Page Token (thuong la vinh vien)."""
    r = requests.get(f"https://graph.facebook.com/{API_VER}/me/accounts", params={
        "access_token": long_user_token,
        "fields": "id,name,access_token",
    })
    data = r.json()
    pages = data.get("data", [])
    for p in pages:
        if p["id"] == PAGE_ID:
            print(f"   Tim thay trang: {p['name']} (ID: {p['id']})")
            return p["access_token"]
    # Neu chi co 1 trang
    if pages:
        p = pages[0]
        print(f"   Su dung trang: {p['name']} (ID: {p['id']})")
        return p["access_token"]
    raise RuntimeError(f"Khong tim thay trang ID {PAGE_ID}. Cac trang: {[p.get('name') for p in pages]}")


def update_env(new_token: str):
    """Cap nhat FB_PAGE_ACCESS_TOKEN trong .env."""
    content = ENV_PATH.read_text(encoding="utf-8")
    import re
    content = re.sub(
        r"FB_PAGE_ACCESS_TOKEN=.*",
        f"FB_PAGE_ACCESS_TOKEN={new_token}",
        content,
    )
    ENV_PATH.write_text(content, encoding="utf-8")
    print("   .env da duoc cap nhat!")


def verify_messenger(token: str) -> bool:
    """Kiem tra token co quyen pages_messaging khong."""
    r = requests.get("https://graph.facebook.com/debug_token", params={
        "input_token": token,
        "access_token": token,
    })
    scopes = r.json().get("data", {}).get("scopes", [])
    return "pages_messaging" in scopes


def main():
    print("=" * 55)
    print("  CHUN STORE — Lay token pages_messaging")
    print("=" * 55)

    # 1. Khoi dong callback server
    server = HTTPServer(("localhost", 8765), CallbackHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    print("\n[1/5] Callback server dang chay tai localhost:8765")

    # 2. Mo OAuth dialog
    oauth_url = (
        f"https://www.facebook.com/{API_VER}/dialog/oauth?"
        + urlencode({
            "client_id":     APP_ID,
            "redirect_uri":  REDIRECT,
            "scope":         SCOPES,
            "response_type": "code",
            "state":         "chunstore",
        })
    )
    print(f"\n[2/5] Mo trinh duyet de cap quyen Messenger...")
    print(f"      (Neu trinh duyet khong tu mo, dan URL nay vao:)")
    print(f"      {oauth_url[:80]}...")
    webbrowser.open(oauth_url)

    # 3. Doi user cap quyen
    print("\n[3/5] Dang cho ban cap quyen tren Facebook...")
    server_done.wait(timeout=120)
    server.shutdown()

    if not received_code:
        print("❌ Het thoi gian cho (120s). Vui long thu lai.")
        sys.exit(1)

    print("   ✅ Da nhan authorization code!")

    # 4. Exchange tokens
    print("\n[4/5] Dang lay Page Token voi quyen Messenger...")
    try:
        short  = exchange_code(received_code)
        long   = to_long_lived(short)
        page_t = get_page_token(long)
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # 5. Kiem tra va luu
    print("\n[5/5] Kiem tra quyen va luu vao .env...")
    has_msg = verify_messenger(page_t)
    if has_msg:
        print("   ✅ Token co quyen pages_messaging!")
    else:
        print("   ⚠️  Token chua co pages_messaging — van tiep tuc luu.")

    update_env(page_t)

    print("\n" + "=" * 55)
    print("✅ HOAN TAT! Token da duoc cap nhat trong .env")
    print("   Buoc tiep theo: chay setup_messenger.py")
    print("=" * 55)


if __name__ == "__main__":
    main()
