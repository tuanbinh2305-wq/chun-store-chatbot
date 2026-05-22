# Chun Store Chatbot — Hướng dẫn cài đặt & deploy

Chatbot Hybrid: **Kịch bản cố định + Claude AI** cho Facebook Messenger.

---

## Cấu trúc file

```
chatbot/
├── webhook.py           ← Flask server nhận tin nhắn FB
├── bot_logic.py         ← Logic hybrid (kịch bản + AI)
├── scenarios.py         ← Kịch bản cố định (keyword → reply)
├── messenger.py         ← Gửi reply về Messenger
├── conversation_db.py   ← SQLite lưu lịch sử chat
├── business_context.py  ← Ngữ cảnh Chun Store cho AI
├── setup_messenger.py   ← Script setup 1 lần
└── requirements.txt     ← Dependencies
```

---

## Bước 1 — Cài dependencies

```bash
cd chatbot
pip install -r requirements.txt
```

---

## Bước 2 — Thêm Anthropic API Key vào .env

Vào https://console.anthropic.com → API Keys → Create Key → Copy key

Mở file `.env` (thư mục gốc), sửa dòng:
```
ANTHROPIC_API_KEY=DIEN_API_KEY_CUA_ANH_VAO_DAY
```
→ Thay bằng key thật (bắt đầu bằng `sk-ant-...`)

---

## Bước 3 — Thêm quyền Messenger vào Meta App

Meta App hiện tại có quyền post bài, cần thêm quyền nhắn tin:

1. Vào https://developers.facebook.com/apps/2373829579812860
2. Thêm product **Messenger** (nếu chưa có)
3. Vào **Messenger > Settings > Access Tokens**
4. Generate token mới với quyền bổ sung:
   - `pages_messaging`
   - `pages_messaging_subscriptions`
5. Cập nhật `FB_PAGE_ACCESS_TOKEN` trong `.env`

---

## Bước 4 — Chạy webhook server

```bash
cd chatbot
python webhook.py
```

Nên thấy:
```
✅ Database khởi tạo xong
✅ Verify token: chunstore_webhook_2026
🚀 Chatbot đang chạy tại http://localhost:5000
```

---

## Bước 5 — Expose ra internet (test local)

Tải ngrok: https://ngrok.com/download

```bash
ngrok http 5000
```

Lấy URL dạng: `https://abc123.ngrok.io`

---

## Bước 6 — Đăng ký Webhook với Facebook

1. Vào https://developers.facebook.com/apps/2373829579812860
2. Messenger > Settings > Webhooks > **Add Callback URL**
3. Callback URL: `https://abc123.ngrok.io/webhook`
4. Verify Token: `chunstore_webhook_2026`
5. Subscribe các event: `messages`, `messaging_postbacks`
6. Chọn Page → Subscribe

---

## Bước 7 — Chạy setup Messenger (1 lần)

```bash
python setup_messenger.py
```

Script này cài:
- Get Started button
- Lời chào khi KH mở Messenger lần đầu
- Persistent Menu (menu cố định)

---

## Deploy Production (Railway — miễn phí)

1. Tạo tài khoản https://railway.app
2. New Project → Deploy from GitHub Repo
3. Thêm env vars trong Railway dashboard
4. Railway tự cấp URL cố định (không cần ngrok)
5. Dùng URL đó đăng ký webhook với Facebook

---

## Thêm/sửa kịch bản

Mở `scenarios.py` → Thêm Scenario mới vào danh sách `SCENARIOS`:

```python
Scenario(
    keywords=["keyword1", "keyword2"],
    response="Nội dung trả lời...",
    quick_replies=["Nút 1", "Nút 2"],  # tùy chọn
),
```

---

## Luồng hoạt động

```
KH nhắn tin
     ↓
[find_scenario()] — tìm keyword trong kịch bản
     ↓
Khớp?
  YES → Trả lời kịch bản ngay (nhanh)
   NO → Gọi Claude AI với context Chun Store + lịch sử chat
     ↓
Gửi reply về Messenger
Lưu vào SQLite
```
