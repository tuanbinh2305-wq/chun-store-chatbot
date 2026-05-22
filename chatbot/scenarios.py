"""
Kịch bản cố định — khớp keyword → trả lời ngay, không cần gọi Claude AI.
Mỗi scenario có: keywords, response, và quick_replies (nút bấm tùy chọn).
"""

from dataclasses import dataclass, field


@dataclass
class Scenario:
    keywords: list[str]
    response: str
    quick_replies: list[str] = field(default_factory=list)


# ──────────────────────────────────────────────
# DANH SÁCH KỊCH BẢN
# ──────────────────────────────────────────────

SCENARIOS: list[Scenario] = [

    # 1. CHÀO HỎI
    Scenario(
        keywords=["chào", "hello", "hi", "alo", "halo", "ơi", "cho hỏi", "tư vấn"],
        response=(
            "Chào chị! 🏠 Em là Chun — nhân viên tư vấn của Chun Store.\n\n"
            "Chun Store chuyên đồ gia dụng Hàn Quốc giúp bếp gọn gàng, "
            "đẹp như phim Hàn mà không cần tốn nhiều công sức ✨\n\n"
            "Chị đang cần tìm hiểu gì ạ?"
        ),
        quick_replies=["📋 Xem bảng giá", "🛍️ Xem combo", "❓ Tư vấn thêm", "🚚 Thông tin ship"],
    ),

    # 2. BẢNG GIÁ
    Scenario(
        keywords=["giá", "bảng giá", "bao nhiêu", "giá bao nhiêu", "tiền", "giá cả", "mắc không", "đắt không", "rẻ không"],
        response=(
            "Dạ bảng giá Chun Store ạ:\n\n"
            "🧊 Khay tủ lạnh: 89.000đ – 149.000đ\n"
            "   → Trong suốt, phân chia ngăn gọn, chịu lạnh -20°C\n\n"
            "🔩 Kệ gia vị dán tường (không khoan): 129.000đ – 199.000đ\n"
            "   → Dán nano, chịu 5kg, gỡ không hỏng tường\n\n"
            "🌀 Hộp gia vị xoay 360°: 169.000đ – 249.000đ\n"
            "   → 8–12 ngăn, tiết kiệm mặt bàn, đẹp như Hàn\n\n"
            "🎁 Combo 3 sản phẩm: 419.000đ – 599.000đ\n"
            "   → Tiết kiệm 30% + Tặng ebook + video hướng dẫn setup\n\n"
            "Chị đang quan tâm sản phẩm nào ạ? Em tư vấn chi tiết hơn nhé 😊"
        ),
        quick_replies=["🎁 Xem combo", "🧊 Khay tủ lạnh", "🔩 Kệ dán tường", "🛒 Đặt hàng ngay"],
    ),

    # 3. COMBO
    Scenario(
        keywords=["combo", "bộ", "set", "mua bộ", "mua combo", "đặt combo"],
        response=(
            "🎁 Combo 3 sản phẩm Chun Store:\n\n"
            "✅ Khay tổ chức tủ lạnh\n"
            "✅ Kệ gia vị dán tường không khoan\n"
            "✅ Hộp gia vị xoay 360°\n\n"
            "💰 Giá combo: 419.000đ – 599.000đ\n"
            "   (Tiết kiệm ~30% so với mua lẻ)\n\n"
            "🎀 Tặng kèm:\n"
            "   • Ebook PDF \"7 ngày bếp đẹp kiểu Hàn\"\n"
            "   • Video hướng dẫn setup từng sản phẩm\n\n"
            "Cả 3 sản phẩm đồng bộ tone trắng/gỗ — bếp nhìn xịn hẳn ạ 🏠✨\n\n"
            "Chị muốn đặt combo không ạ?"
        ),
        quick_replies=["🛒 Đặt combo ngay", "📸 Xem hình sản phẩm", "🚚 Phí ship bao nhiêu"],
    ),

    # 4. SHIP / GIAO HÀNG
    Scenario(
        keywords=["ship", "giao hàng", "vận chuyển", "phí ship", "cod", "thu hộ", "giao nhanh", "giao bao lâu", "freeship"],
        response=(
            "🚚 Thông tin giao hàng Chun Store:\n\n"
            "• Ship COD toàn quốc (trả tiền khi nhận hàng)\n"
            "• Phí ship: 25.000đ – 35.000đ tùy khu vực\n"
            "• Miễn phí ship cho đơn từ 499.000đ ✅\n"
            "• Thời gian giao:\n"
            "   - Nội thành HN/HCM: 1–2 ngày\n"
            "   - Tỉnh gần: 2–3 ngày\n"
            "   - Tỉnh xa (miền Tây, Tây Nguyên): 3–5 ngày\n\n"
            "Chị ở khu vực nào để em báo chính xác hơn ạ?"
        ),
        quick_replies=["🛒 Đặt hàng", "💰 Xem bảng giá", "❓ Hỏi thêm"],
    ),

    # 5. NHÀ THUÊ / KHÔNG KHOAN
    Scenario(
        keywords=["nhà thuê", "thuê nhà", "không khoan", "không được khoan", "dán", "dán tường", "trả phòng", "tiền cọc"],
        response=(
            "Chị đang thuê nhà không cần lo về khoan tường nha ạ! 🏠✅\n\n"
            "Kệ gia vị của Chun Store dùng công nghệ dán nano:\n"
            "• Dán chắc — chịu 5kg\n"
            "• Gỡ sạch khi trả phòng — KHÔNG để lại vết, không hỏng tường\n"
            "• Chất liệu inox 304 — chống nước, bếp dầu mỡ không sao\n\n"
            "Nhiều chị thuê nhà dùng sản phẩm này xong còn tiếc không mua sớm hơn á 😄\n\n"
            "Chị muốn xem hình thực tế hay xem giá ạ?"
        ),
        quick_replies=["💰 Xem giá kệ dán", "🛒 Đặt hàng", "📸 Xem hình thực tế"],
    ),

    # 6. ĐẶT HÀNG
    Scenario(
        keywords=["đặt hàng", "đặt", "mua", "order", "mình mua", "cho mình đặt", "muốn mua"],
        response=(
            "Dạ để em hỗ trợ chị đặt hàng ạ! 🛒\n\n"
            "Chị cho em biết:\n"
            "1️⃣ Sản phẩm muốn mua (khay tủ lạnh / kệ dán / hộp xoay / combo)\n"
            "2️⃣ Tên người nhận\n"
            "3️⃣ Số điện thoại\n"
            "4️⃣ Địa chỉ giao hàng (số nhà, đường, phường/xã, quận/huyện, tỉnh/thành)\n\n"
            "Em sẽ xác nhận đơn và báo phí ship sau ạ 😊"
        ),
        quick_replies=["🎁 Muốn mua combo", "🧊 Muốn mua khay tủ lạnh", "🔩 Muốn mua kệ dán tường"],
    ),

    # 7. ĐỔI TRẢ / CHÍNH SÁCH
    Scenario(
        keywords=["đổi trả", "hoàn tiền", "trả hàng", "bảo hành", "chính sách", "lỗi", "hỏng", "không giống hình"],
        response=(
            "Dạ chính sách Chun Store ạ:\n\n"
            "🔄 Đổi trả trong 7 ngày nếu:\n"
            "   • Sản phẩm lỗi do nhà sản xuất\n"
            "   • Sản phẩm không đúng với mô tả\n"
            "   • Giao nhầm hàng\n\n"
            "📦 Quy trình:\n"
            "   • Chị quay video unbox lúc nhận hàng\n"
            "   • Nếu có vấn đề → nhắn cho em kèm video\n"
            "   • Em hỗ trợ đổi/hoàn trong 1-2 ngày làm việc\n\n"
            "Chun Store cam kết hàng đúng hình, đúng chất lượng ạ 💪\n\n"
            "Chị đang gặp vấn đề gì với đơn hàng không ạ?"
        ),
        quick_replies=["📦 Đơn hàng đang gặp vấn đề", "❓ Hỏi thêm", "🛒 Muốn đặt hàng"],
    ),

    # 8. CHẤT LIỆU / NGUỒN GỐC
    Scenario(
        keywords=["chất liệu", "nguyên liệu", "nhựa", "inox", "an toàn", "hàn quốc", "xuất xứ", "nguồn gốc", "chính hãng"],
        response=(
            "Dạ chất liệu sản phẩm Chun Store ạ:\n\n"
            "🧊 Khay tủ lạnh:\n"
            "   • Nhựa PP cao cấp — an toàn thực phẩm, không BPA\n"
            "   • Chịu nhiệt độ -20°C đến 120°C\n\n"
            "🔩 Kệ dán tường:\n"
            "   • Inox 304 — không gỉ, chống nước, chịu dầu mỡ bếp\n"
            "   • Keo dán nano — chịu lực 5kg\n\n"
            "🌀 Hộp gia vị:\n"
            "   • Nhựa ABS + PP — an toàn, bền, chống va đập\n\n"
            "Sản phẩm nhập từ Hàn Quốc, có kiểm định chất lượng 🇰🇷✅\n\n"
            "Chị muốn xem thêm thông tin gì ạ?"
        ),
        quick_replies=["💰 Xem giá", "🛒 Đặt hàng", "🚚 Thông tin ship"],
    ),
]


# ──────────────────────────────────────────────
# HÀM TÌM KỊCH BẢN KHỚP
# ──────────────────────────────────────────────

import re as _re
import unicodedata


def _no_accent(text: str) -> str:
    """
    Bỏ dấu tiếng Việt + lowercase.
    Dùng NFD decomposition: tách ký tự + combining mark → bỏ combining mark.
    'đ'/'Đ' xử lý riêng vì không phân rã qua NFD.
    """
    text = text.replace("đ", "d").replace("Đ", "D")
    nfd = unicodedata.normalize("NFD", text)
    # Giữ lại ký tự không phải combining mark (category Mn)
    result = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return result.lower().strip()


def normalize(text: str) -> str:
    """Chuẩn hóa text để so sánh: bỏ dấu + lowercase + padding."""
    return " " + _no_accent(text) + " "


def _kw_pattern(keyword: str) -> _re.Pattern:
    """
    Tạo regex khớp keyword ở ranh giới từ.
    Hỗ trợ cả từ tiếng Việt (có dấu) lẫn emoji.
    Dùng (?<![\\w]) và (?![\\w]) thay vì \\b vì \\b không hiểu Unicode.
    """
    escaped = _re.escape(keyword)
    return _re.compile(r"(?<!\w)" + escaped + r"(?!\w)", _re.IGNORECASE)


# Cache pattern để không compile lại mỗi lần
_PATTERN_CACHE: dict[str, _re.Pattern] = {}


def find_scenario(message: str) -> "Scenario | None":
    """
    Tìm kịch bản khớp với tin nhắn.
    Dùng word-boundary matching để tránh false positive.
    Trả về Scenario nếu khớp, None nếu không khớp (→ gọi Claude AI).
    """
    msg = normalize(message)  # bỏ dấu + lowercase
    for scenario in SCENARIOS:
        for keyword in scenario.keywords:
            kw = _no_accent(keyword)  # cũng bỏ dấu keyword để so sánh đồng nhất
            # Keyword ngắn ≤ 3 ký tự → word-boundary để tránh false positive
            if len(kw) <= 3:
                pat = _PATTERN_CACHE.setdefault(kw, _kw_pattern(kw))
                if pat.search(msg):
                    return scenario
            else:
                if kw in msg:
                    return scenario
    return None
