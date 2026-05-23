# SOP: Deploy Chatbot Facebook Messenger lên Render.com

> Quy trình chi tiết từ A-Z để deploy chatbot Chun Store lên Render (free tier), kết nối Facebook Messenger, và duy trì hoạt động 24/7.

---

## Mục lục
1. [Chuẩn bị](#1-chuẩn-bị)
2. [Push code lên GitHub](#2-push-code-lên-github)
3. [Tạo Web Service trên Render](#3-tạo-web-service-trên-render)
4. [Cấu hình Environment Variables trên Render](#4-cấu-hình-environment-variables-trên-render)
5. [Cập nhật Webhook URL trên Facebook Developer](#5-cập-nhật-webhook-url-trên-facebook-developer)
6. [Chuyển Facebook App sang Live Mode](#6-chuyển-facebook-app-sang-live-mode)
7. [Setup UptimeRobot (chống Render ngủ)](#7-setup-uptimerobot-chống-render-ngủ)
8. [Đổi AI Model (Claude / Gemini)](#8-đổi-ai-model-claude--gemini)
9. [Xử lý sự cố thường gặp](#9-xử-lý-sự-cố-thường-gặp)

---

## 1. Chuẩn bị

### Tài khoản cần có:
- **GitHub** — để lưu code (public repo)
- **Render.com** — để host bot (free tier)
- **Facebook Developer** — để cấu hình webhook Messenger
- **Anthropic** (console.anthropic.com) — để lấy Claude API key
- **UptimeRobot** — để ping bot mỗi 5 phút (free)

### Cấu trúc code chatbot:
```
chatbot/
├── webhook.py          ← Flask server nhận webhook Facebook
├── bot_logic.py        ← Logic chính (kịch bản + AI)
├── scenarios.py        ← Kịch bản trả lời cố định
├── business_context.py ← System prompt cho AI
├── conversation_db.py  ← Lưu lịch sử chat (SQLite)
├── messenger.py        ← Gọi Facebook Messenger API
├── requirements.txt    ← Thư viện Python cần thiết
└── setup_messenger.py  ← Setup persistent menu
Procfile                ← Lệnh khởi động cho Render
```

### File cấu hình quan trọng:

**requirements.txt:**
```
flask>=3.0.0
anthropic>=0.25.0
requests>=2.31.0
python-dotenv>=1.0.0
```

**Procfile** (nằm ở root, không phải trong chatbot/):
```
web: python chatbot/webhook.py
```

---

## 2. Push code lên GitHub

### Bước 2.1 — Tạo repo trên GitHub
1. Vào github.com → New repository
2. Đặt tên: `chun-store-chatbot`
3. Chọn **Public** (Render free chỉ hỗ trợ public repo)
4. KHÔNG tick "Add README" (đã có sẵn)

### Bước 2.2 — Push code từ máy
```bash
cd "D:\Não Chun\Não Chun Nè"
git init
git add chatbot/ Procfile requirements.txt
git commit -m "feat: chatbot Facebook Messenger Chun Store"
git remote add origin https://github.com/<username>/chun-store-chatbot.git
git push -u origin main
```

### Bước 2.3 — Kiểm tra .gitignore
Đảm bảo file `.gitignore` có:
```
.env
chatbot/conversations.db
chatbot/__pycache__/
```
→ **KHÔNG BAO GIỜ** push file `.env` (chứa API key) lên GitHub!

---

## 3. Tạo Web Service trên Render

### Bước 3.1 — Đăng nhập Render
1. Vào https://render.com → Sign in bằng GitHub

### Bước 3.2 — Tạo Web Service mới
1. Click **"+ New"** → **"Web Service"**
2. Chọn **"Build and deploy from a Git repository"**
3. Kết nối repo GitHub `chun-store-chatbot`
4. Cấu hình:
   - **Name:** `chun-store-chatbot`
   - **Region:** Singapore (gần Việt Nam nhất)
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r chatbot/requirements.txt`
   - **Start Command:** `python chatbot/webhook.py`
   - **Instance Type:** `Free`
5. Click **"Create Web Service"**

### Bước 3.3 — Chờ deploy
- Build mất khoảng 2-5 phút
- Khi xong sẽ thấy: `==> Your service is live`
- URL sẽ là: `https://chun-store-chatbot.onrender.com`

---

## 4. Cấu hình Environment Variables trên Render

### Bước 4.1 — Vào Environment
1. Trên Render dashboard → chọn service `chun-store-chatbot`
2. Sidebar trái → **Environment**
3. Click **"Edit"**

### Bước 4.2 — Thêm các biến
Thêm từng biến sau (click "+ Add variable"):

| KEY | VALUE | Ghi chú |
|-----|-------|---------|
| `ANTHROPIC_API_KEY` | `sk-ant-...` | Lấy từ console.anthropic.com → API Keys |
| `FB_APP_ID` | `...` | Facebook Developer → App Settings → Basic |
| `FB_APP_SECRET` | `...` | Facebook Developer → App Settings → Basic |
| `FB_PAGE_ACCESS_TOKEN` | `...` | Facebook Developer → Messenger → Settings → Token Generation |
| `FB_PAGE_ID` | `...` | ID của Facebook Page |
| `FB_VERIFY_TOKEN` | `chunstore_webhook_2026` | Tự đặt, phải khớp với code |

### Bước 4.3 — Lưu và deploy
1. Click **"Save, rebuild, and deploy"**
2. Chờ deploy xong (1-2 phút)

---

## 5. Cập nhật Webhook URL trên Facebook Developer

### Bước 5.1 — Vào Facebook Developer
1. Truy cập https://developers.facebook.com
2. Chọn App → Messenger → Settings

### Bước 5.2 — Cấu hình Webhook
1. Trong phần **Webhooks** → Click **"Edit Callback URL"**
2. Điền:
   - **Callback URL:** `https://chun-store-chatbot.onrender.com/webhook`
   - **Verify Token:** `chunstore_webhook_2026` (phải khớp với env var)
3. Click **"Verify and Save"**

### Bước 5.3 — Subscribe events
1. Sau khi verify thành công → Click **"Add Subscriptions"**
2. Tick chọn:
   - `messages`
   - `messaging_postbacks`
   - `messaging_optins`
3. Click **"Save"**

---

## 6. Chuyển Facebook App sang Live Mode

### Bước 6.1 — Tạo Privacy Policy
1. Vào https://www.termsfeed.com/privacy-policy-generator/
2. Tạo Privacy Policy miễn phí cho shop
3. Download link URL của Privacy Policy

### Bước 6.2 — Thêm Privacy Policy vào App
1. Facebook Developer → App Settings → Basic
2. Dán URL Privacy Policy vào ô **"Privacy Policy URL"**
3. Click **"Save Changes"**

### Bước 6.3 — Chuyển sang Live Mode
1. Sidebar trái → tìm mục **"Đăng"** (hoặc "Go Live")
2. Click vào **"Đăng"**
3. Xác nhận → Khi thấy **"Đã đăng" ✅** là xong

> **Lưu ý:** Nếu không thấy nút "Đăng", kiểm tra:
> - Privacy Policy URL đã điền chưa
> - App có ít nhất 1 product (Messenger) đã cấu hình

---

## 7. Setup UptimeRobot (chống Render ngủ)

> Render free tier sẽ **tắt server sau 15 phút** không có request. UptimeRobot ping mỗi 5 phút để giữ bot luôn thức.

### Bước 7.1 — Tạo tài khoản
1. Vào https://uptimerobot.com → Sign Up (free)

### Bước 7.2 — Tạo Monitor
1. Click **"+ Add New Monitor"**
2. Cấu hình:
   - **Monitor Type:** `HTTP(s)`
   - **Friendly Name:** `Chun Store Chatbot`
   - **URL:** `https://chun-store-chatbot.onrender.com`
   - **Monitoring Interval:** `5 minutes`
3. Click **"Create Monitor"**

### Bước 7.3 — Xác nhận
- Status hiện **"Up"** = hoạt động tốt
- Bot sẽ không bao giờ bị ngủ nữa

---

## 8. Đổi AI Model (Claude / Gemini)

### Đổi sang Claude AI:

**Bước 1 — Sửa `requirements.txt`:**
```
anthropic>=0.25.0
```
(Xóa dòng `google-generativeai` nếu có)

**Bước 2 — Sửa `bot_logic.py`:**
- Import: `import anthropic`
- Model: `claude-3-5-haiku-20241022` (nhanh, rẻ cho chatbot)
- API call dùng `client.messages.create()`

**Bước 3 — Environment trên Render:**
- Thêm `ANTHROPIC_API_KEY`
- Xóa `GEMINI_API_KEY` (nếu có)

**Bước 4 — Push và deploy:**
```bash
git add chatbot/bot_logic.py chatbot/requirements.txt
git commit -m "feat: đổi sang Claude AI"
git push
```
→ Render tự động deploy khi code push lên GitHub.

---

### Đổi sang Gemini AI (miễn phí):

**Bước 1 — Lấy API key:**
1. Vào https://aistudio.google.com/apikey
2. Click "Create API Key" → copy key

**Bước 2 — Sửa `requirements.txt`:**
```
google-generativeai>=0.8.0
```
(Xóa dòng `anthropic` nếu có)

**Bước 3 — Sửa `bot_logic.py`:**
- Import: `import google.generativeai as genai`
- Model: `gemini-2.0-flash`
- Lưu ý format history: role `"model"` (không phải `"assistant"`)

**Bước 4 — Environment trên Render:**
- Thêm `GEMINI_API_KEY`
- Xóa `ANTHROPIC_API_KEY` (nếu có)

> **Lưu ý Gemini free tier:**
> - Giới hạn 1.500 request/ngày
> - Giới hạn 15 request/phút
> - Nếu bị quota exceeded → chờ đến 7h sáng (reset lúc 0h UTC)

---

## 9. Xử lý sự cố thường gặp

### Bot trả lời "sự cố kỹ thuật"
**Nguyên nhân:** AI API lỗi (hết credit, quota, key sai)
**Kiểm tra:**
1. Render → Logs → tìm dòng `[bot_logic] Claude lỗi:` hoặc `Gemini lỗi:`
2. Đọc lỗi cụ thể:
   - `credit balance is too low` → nạp thêm tiền Anthropic
   - `quota exceeded` (Gemini) → chờ reset hoặc tạo key mới
   - `authentication_error` → API key sai, kiểm tra lại

### Bot không phản hồi gì cả
**Kiểm tra:**
1. Webhook URL đúng chưa? (Facebook Developer → Messenger → Webhooks)
2. App đang ở Live Mode chưa? (không phải Development)
3. Page Access Token còn hạn không?
4. Render service có đang chạy không? (Logs → có request HEAD mỗi 5 phút)

### Render deploy thất bại
**Kiểm tra:**
1. `requirements.txt` có đúng tên package không?
2. `Procfile` có đúng đường dẫn không? (`web: python chatbot/webhook.py`)
3. Code có lỗi syntax không? (test local trước: `python chatbot/webhook.py`)

### Cập nhật Environment Variable
1. Render → service → Environment → Edit
2. Sửa value → click **"Save, rebuild, and deploy"**
3. Chờ 1-2 phút cho deploy mới

---

## Checklist nhanh khi deploy lần đầu

- [ ] Code đã push lên GitHub (public repo)
- [ ] Render Web Service đã tạo, đang chạy
- [ ] 6 Environment Variables đã cấu hình (ANTHROPIC_API_KEY, FB_APP_ID, FB_APP_SECRET, FB_PAGE_ACCESS_TOKEN, FB_PAGE_ID, FB_VERIFY_TOKEN)
- [ ] Webhook URL đã cập nhật trên Facebook Developer
- [ ] Facebook App đã chuyển sang Live Mode
- [ ] UptimeRobot đã setup ping mỗi 5 phút
- [ ] Test nhắn tin vào Page → bot phản hồi đúng

---

*Cập nhật lần cuối: 2026-05-23*
*Thực hiện bởi: Claude AI + Anh Chun*
