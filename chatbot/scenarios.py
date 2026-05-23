"""
Kịch bản cố định — khớp keyword → trả lời ngay, không cần gọi Claude AI.
Mỗi scenario có: keywords, response, và quick_replies (nút bấm tùy chọn).

Mục tiêu: Cover 80-90% câu hỏi phổ biến bằng kịch bản
→ Giảm tối đa gọi Claude AI (tốn tiền)
→ Trả lời nhanh hơn (không chờ AI)
→ Kiểm soát chất lượng câu trả lời

Lưu ý keyword:
- Bao gồm cả dạng viết tắt (bn, sdt, k, ko, mk, j)
- Bao gồm cả dạng không dấu (gia, bao nhieu)
- Thứ tự SCENARIOS quan trọng: scenario đầu khớp trước sẽ được dùng
"""

from dataclasses import dataclass, field


@dataclass
class Scenario:
    keywords: list[str]
    response: str
    quick_replies: list[str] = field(default_factory=list)


# ──────────────────────────────────────────────
# DANH SÁCH KỊCH BẢN (thứ tự = độ ưu tiên)
# ──────────────────────────────────────────────

SCENARIOS: list[Scenario] = [

    # ═══════════════════════════════════════════
    # NHÓM 1: ĐẶT HÀNG & MUA (ưu tiên cao nhất)
    # ═══════════════════════════════════════════

    # 1. ĐẶT HÀNG
    Scenario(
        keywords=[
            "đặt hàng", "đặt", "order", "mình mua", "cho mình đặt",
            "muốn mua", "mua ngay", "lấy", "cho em đặt", "đặt cho mình",
            "mua hàng", "dat hang", "mua luon", "mua liền", "chốt",
            "cho chị đặt", "muốn đặt", "đặt nha", "đặt nhé",
        ],
        response=(
            "Dạ để em hỗ trợ chị đặt hàng ạ! 🛒\n\n"
            "Chị cho em biết:\n"
            "1️⃣ Sản phẩm muốn mua (khay tủ lạnh / kệ dán / hộp xoay / combo)\n"
            "2️⃣ Tên người nhận\n"
            "3️⃣ Số điện thoại\n"
            "4️⃣ Địa chỉ giao hàng\n\n"
            "Em sẽ xác nhận đơn và báo phí ship sau ạ 😊"
        ),
        quick_replies=["🎁 Muốn mua combo", "🧊 Muốn mua khay tủ lạnh", "🔩 Muốn mua kệ dán tường"],
    ),

    # 2. MUỐN MUA COMBO
    Scenario(
        keywords=["muốn mua combo", "đặt combo", "lấy combo", "chốt combo", "mua bộ"],
        response=(
            "Chị chọn combo đúng rồi — tiết kiệm nhất luôn ạ! 🎁\n\n"
            "💰 Combo 3 SP: 419.000đ – 599.000đ (tiết kiệm ~30%)\n"
            "📦 Bao gồm: Khay tủ lạnh + Kệ dán + Hộp xoay\n"
            "🎀 Tặng kèm: Ebook + Video hướng dẫn setup\n"
            "🚚 Freeship cho đơn từ 499K\n\n"
            "Chị cho em thông tin để đặt nhé:\n"
            "• Tên người nhận\n"
            "• SĐT\n"
            "• Địa chỉ giao hàng"
        ),
        quick_replies=["📋 Xem bảng giá", "🚚 Thông tin ship"],
    ),

    # 3. MUỐN MUA KHAY TỦ LẠNH
    Scenario(
        keywords=["muốn mua khay tủ lạnh", "mua khay", "lấy khay", "đặt khay"],
        response=(
            "Dạ khay tủ lạnh bên em có nhiều size ạ:\n\n"
            "📏 Size S (nhỏ): 89.000đ — vừa ngăn nhỏ\n"
            "📏 Size M (trung): 109.000đ — phổ biến nhất\n"
            "📏 Size L (lớn): 149.000đ — ngăn rau củ\n\n"
            "✅ Nhựa PP an toàn, chịu lạnh -20°C\n"
            "✅ Trong suốt, dễ nhìn thực phẩm\n\n"
            "Chị muốn lấy size nào ạ? Cho em thêm:\n"
            "• Tên người nhận\n"
            "• SĐT\n"
            "• Địa chỉ giao hàng"
        ),
        quick_replies=["🎁 Xem combo tiết kiệm hơn", "🚚 Phí ship bao nhiêu"],
    ),

    # 4. MUỐN MUA KỆ DÁN TƯỜNG
    Scenario(
        keywords=["muốn mua kệ dán tường", "muốn mua kệ", "mua kệ", "lấy kệ", "đặt kệ"],
        response=(
            "Dạ kệ dán tường bên em có 2 loại ạ:\n\n"
            "🔩 Kệ 1 tầng: 129.000đ — gọn gàng\n"
            "🔩 Kệ 2 tầng: 199.000đ — để được nhiều hơn\n\n"
            "✅ Inox 304 chống gỉ, chống nước\n"
            "✅ Dán nano chịu 5kg — gỡ không hỏng tường\n"
            "✅ Phù hợp nhà thuê, không cần khoan\n\n"
            "Chị muốn lấy loại nào ạ? Cho em thêm:\n"
            "• Tên người nhận\n"
            "• SĐT\n"
            "• Địa chỉ giao hàng"
        ),
        quick_replies=["🎁 Xem combo tiết kiệm hơn", "🚚 Phí ship bao nhiêu"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 2: THÔNG TIN SẢN PHẨM & GIÁ
    # ═══════════════════════════════════════════

    # 5. BẢNG GIÁ
    Scenario(
        keywords=[
            "giá", "bảng giá", "bao nhiêu", "giá bao nhiêu", "tiền",
            "giá cả", "mắc không", "đắt không", "rẻ không", "bn",
            "bao nhieu", "gia bao nhieu", "giá tiền", "bảng giá",
            "inbox giá", "pm giá", "báo giá",
        ],
        response=(
            "Dạ bảng giá Chun Store ạ:\n\n"
            "🧊 Khay tủ lạnh: 89K – 149K\n"
            "🔩 Kệ dán tường (không khoan): 129K – 199K\n"
            "🌀 Hộp gia vị xoay 360°: 169K – 249K\n"
            "🎁 Combo 3 SP: 419K – 599K (tiết kiệm 30%)\n\n"
            "👉 Mua combo tiết kiệm nhất + được tặng ebook & video hướng dẫn setup ạ!\n\n"
            "Chị quan tâm sản phẩm nào ạ?"
        ),
        quick_replies=["🎁 Xem combo", "🛒 Đặt hàng ngay", "🚚 Thông tin ship"],
    ),

    # 6. COMBO
    Scenario(
        keywords=["combo", "bộ", "set", "mua combo", "xem combo"],
        response=(
            "🎁 Combo 3 sản phẩm Chun Store:\n\n"
            "✅ Khay tổ chức tủ lạnh\n"
            "✅ Kệ gia vị dán tường không khoan\n"
            "✅ Hộp gia vị xoay 360°\n\n"
            "💰 Giá combo: 419K – 599K (tiết kiệm ~30%)\n\n"
            "🎀 Tặng kèm:\n"
            "• Ebook \"7 ngày bếp đẹp kiểu Hàn\"\n"
            "• Video hướng dẫn setup\n\n"
            "Cả 3 đồng bộ tone trắng/gỗ — bếp nhìn xịn hẳn ạ 🏠✨\n\n"
            "Chị muốn đặt combo không ạ?"
        ),
        quick_replies=["🛒 Đặt combo ngay", "🚚 Phí ship bao nhiêu", "📋 Xem bảng giá"],
    ),

    # 7. KÍCH THƯỚC / SIZE
    Scenario(
        keywords=[
            "kích thước", "size", "kích cỡ", "bao lớn", "bao to",
            "dài bao nhiêu", "rộng bao nhiêu", "cao bao nhiêu",
            "vừa tủ không", "vừa bếp không",
        ],
        response=(
            "Dạ kích thước chi tiết ạ:\n\n"
            "🧊 Khay tủ lạnh:\n"
            "• S: 15×10×6 cm — ngăn nhỏ, để trứng/gia vị\n"
            "• M: 25×15×8 cm — phổ biến, để rau/trái cây\n"
            "• L: 32×20×10 cm — ngăn rau củ lớn\n\n"
            "🔩 Kệ dán tường:\n"
            "• 1 tầng: 40×12×10 cm\n"
            "• 2 tầng: 40×12×25 cm\n\n"
            "🌀 Hộp xoay: đường kính 25cm, cao 20cm\n\n"
            "Chị cho em biết tủ lạnh/bếp chị rộng bao nhiêu, em tư vấn size phù hợp nhé!"
        ),
        quick_replies=["💰 Xem giá", "🛒 Đặt hàng", "❓ Tư vấn thêm"],
    ),

    # 8. CHẤT LIỆU / NGUỒN GỐC
    Scenario(
        keywords=[
            "chất liệu", "nguyên liệu", "nhựa", "inox", "an toàn",
            "hàn quốc", "xuất xứ", "nguồn gốc", "chính hãng",
            "có độc không", "bpa", "chat lieu",
        ],
        response=(
            "Dạ chất liệu sản phẩm Chun Store ạ:\n\n"
            "🧊 Khay tủ lạnh:\n"
            "• Nhựa PP — an toàn thực phẩm, không BPA\n"
            "• Chịu -20°C đến 120°C\n\n"
            "🔩 Kệ dán tường:\n"
            "• Inox 304 — không gỉ, chống nước\n"
            "• Keo nano — chịu 5kg, gỡ sạch\n\n"
            "🌀 Hộp gia vị:\n"
            "• Nhựa ABS + PP — bền, chống va đập\n\n"
            "Sản phẩm nhập Hàn Quốc, có kiểm định chất lượng 🇰🇷✅\n\n"
            "Chị muốn xem gì thêm ạ?"
        ),
        quick_replies=["💰 Xem giá", "🛒 Đặt hàng", "🚚 Thông tin ship"],
    ),

    # 9. HÌNH ẢNH / REVIEW
    Scenario(
        keywords=[
            "hình", "ảnh", "hình ảnh", "xem hình", "cho xem", "review",
            "đánh giá", "feedback", "hình thực tế", "có hình không",
            "hinh", "anh", "xem anh", "cho xem hinh", "có ảnh không",
            "hình thật", "ảnh thật", "before after",
        ],
        response=(
            "Dạ chị xem hình thực tế và review từ khách đã mua ạ! 📸\n\n"
            "👉 Hình sản phẩm + before/after: chị xem trên page Chun Store nhé ạ\n\n"
            "⭐ Feedback từ khách:\n"
            "• \"Tủ lạnh gọn hẳn, mở ra thấy sướng mắt\" — Chị Linh, HN\n"
            "• \"Nhà thuê mà bếp đẹp như phim Hàn\" — Chị Nga, SG\n"
            "• \"Mua combo xong còn mua thêm tặng mẹ\" — Chị Trang, ĐN\n\n"
            "Chị muốn đặt thử không ạ? Không ưng đổi trả trong 7 ngày luôn 😊"
        ),
        quick_replies=["🛒 Đặt hàng", "💰 Xem giá", "🔄 Chính sách đổi trả"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 3: VẬN CHUYỂN & CHÍNH SÁCH
    # ═══════════════════════════════════════════

    # 10. SHIP / GIAO HÀNG
    Scenario(
        keywords=[
            "ship", "giao hàng", "vận chuyển", "phí ship", "cod",
            "thu hộ", "giao nhanh", "giao bao lâu", "freeship",
            "phi ship", "free ship", "miễn phí ship", "mien phi ship",
            "bao lâu nhận", "bao gio nhan", "mấy ngày",
        ],
        response=(
            "🚚 Thông tin giao hàng ạ:\n\n"
            "• Ship COD toàn quốc (nhận hàng mới trả tiền)\n"
            "• Phí ship: 25K – 35K tùy khu vực\n"
            "• 🎉 FREE ship cho đơn từ 499K\n"
            "• Thời gian giao:\n"
            "  - HN/HCM: 1–2 ngày\n"
            "  - Tỉnh gần: 2–3 ngày\n"
            "  - Tỉnh xa: 3–5 ngày\n\n"
            "👉 Mua combo 499K+ là freeship luôn ạ!\n\n"
            "Chị ở khu vực nào ạ?"
        ),
        quick_replies=["🛒 Đặt hàng", "🎁 Xem combo freeship", "💰 Xem bảng giá"],
    ),

    # 11. ĐỔI TRẢ / BẢO HÀNH
    Scenario(
        keywords=[
            "đổi trả", "hoàn tiền", "trả hàng", "bảo hành", "chính sách",
            "lỗi", "hỏng", "không giống hình", "đổi", "trả",
            "doi tra", "bao hanh", "chinh sach",
        ],
        response=(
            "Dạ chính sách Chun Store ạ:\n\n"
            "🔄 Đổi trả trong 7 ngày nếu:\n"
            "• Sản phẩm lỗi do nhà sản xuất\n"
            "• Không đúng mô tả\n"
            "• Giao nhầm hàng\n\n"
            "📦 Quy trình:\n"
            "• Quay video unbox lúc nhận hàng\n"
            "• Có vấn đề → nhắn em kèm video\n"
            "• Em đổi/hoàn trong 1-2 ngày\n\n"
            "Cam kết hàng đúng hình, đúng chất lượng ạ 💪"
        ),
        quick_replies=["🛒 Đặt hàng", "💰 Xem giá", "❓ Hỏi thêm"],
    ),

    # 12. NHÀ THUÊ / KHÔNG KHOAN
    Scenario(
        keywords=[
            "nhà thuê", "thuê nhà", "không khoan", "không được khoan",
            "dán", "dán tường", "trả phòng", "tiền cọc", "nha thue",
            "khoan tường", "sợ hỏng tường",
        ],
        response=(
            "Chị thuê nhà không cần lo khoan tường ạ! 🏠✅\n\n"
            "Kệ dán Chun Store dùng keo nano:\n"
            "• Dán chắc — chịu 5kg\n"
            "• Gỡ sạch — KHÔNG để vết, không mất cọc\n"
            "• Inox 304 — chống nước, dầu mỡ OK\n\n"
            "Nhiều chị thuê nhà dùng xong còn tiếc không mua sớm hơn 😄\n\n"
            "Chị muốn xem giá hay đặt luôn ạ?"
        ),
        quick_replies=["💰 Xem giá kệ dán", "🛒 Đặt hàng", "🎁 Xem combo"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 4: KHUYẾN MÃI & SO SÁNH
    # ═══════════════════════════════════════════

    # 13. KHUYẾN MÃI / GIẢM GIÁ
    Scenario(
        keywords=[
            "khuyến mãi", "giảm giá", "sale", "ưu đãi", "mã giảm",
            "voucher", "coupon", "discount", "khuyen mai", "giam gia",
            "có giảm không", "có sale không", "có khuyến mãi không",
        ],
        response=(
            "Dạ hiện tại Chun Store có ưu đãi ạ:\n\n"
            "🎁 Combo 3 SP — tiết kiệm 30% so với mua lẻ\n"
            "🚚 FREE ship cho đơn từ 499K\n"
            "📚 Tặng kèm Ebook + Video hướng dẫn setup\n\n"
            "👉 Combo là deal tốt nhất hiện tại ạ — vừa tiết kiệm vừa được freeship + quà tặng!\n\n"
            "Chị muốn xem combo không ạ?"
        ),
        quick_replies=["🎁 Xem combo", "💰 Xem bảng giá", "🛒 Đặt hàng"],
    ),

    # 14. SO SÁNH / TỐT HƠN GÌ
    Scenario(
        keywords=[
            "so sánh", "khác gì", "hơn gì", "tốt hơn", "shopee",
            "lazada", "tiki", "ngoài chợ", "ngoài tiệm",
            "mua ở đâu rẻ hơn", "bên khác", "hàng tàu",
        ],
        response=(
            "Dạ chị hỏi rất hay! So sánh Chun Store với hàng chợ/Shopee ạ:\n\n"
            "🏷️ Hàng chợ/Shopee:\n"
            "• Rẻ hơn 20-30K nhưng nhựa mỏng, dễ vỡ\n"
            "• Không rõ nguồn gốc, có thể chứa BPA\n"
            "• Không bảo hành, không đổi trả\n\n"
            "✅ Chun Store:\n"
            "• Nhập Hàn Quốc, kiểm định chất lượng\n"
            "• Nhựa PP an toàn, không BPA\n"
            "• Đổi trả 7 ngày + CSKH 7 ngày sau mua\n"
            "• Mua combo tiết kiệm 30% + quà tặng\n\n"
            "Chênh vài chục K nhưng dùng an tâm hơn nhiều ạ 😊"
        ),
        quick_replies=["🎁 Xem combo", "🛒 Đặt hàng", "📋 Xem bảng giá"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 5: LIÊN HỆ & HỖ TRỢ
    # ═══════════════════════════════════════════

    # 15. SĐT / HOTLINE
    Scenario(
        keywords=[
            "sdt", "số điện thoại", "hotline", "liên hệ", "gọi",
            "phone", "zalo", "so dien thoai", "lien he", "gọi cho ai",
            "sđt", "điện thoại",
        ],
        response=(
            "Dạ chị liên hệ Chun Store qua:\n\n"
            "📱 Nhắn tin: m.me/ChunStore (nhanh nhất)\n"
            "📞 Zalo: 0xxx.xxx.xxx\n"
            "⏰ Thời gian hỗ trợ: 8h – 21h hàng ngày\n\n"
            "Hoặc chị cứ nhắn tại đây, em hỗ trợ ngay ạ! 😊"
        ),
        quick_replies=["💰 Xem giá", "🛒 Đặt hàng", "❓ Hỏi thêm"],
    ),

    # 16. BẾP NHỎ / BẾP BỪA
    Scenario(
        keywords=[
            "bếp nhỏ", "bếp chật", "bếp bừa", "bừa bộn", "ngán",
            "tủ lạnh bừa", "đồ ngập", "không có chỗ", "hết chỗ",
            "bep nho", "bep bua", "tu lanh bua",
        ],
        response=(
            "Em hiểu chị luôn ạ — bếp nhỏ mà đồ cứ ngập lên! 😅\n\n"
            "Giải pháp Chun Store cho bếp 4-6m²:\n\n"
            "🧊 Khay tủ lạnh: Phân chia ngăn gọn, nhìn vào biết có gì\n"
            "🔩 Kệ dán tường: Tận dụng tường trống, không chiếm mặt bàn\n"
            "🌀 Hộp xoay: 8-12 ngăn trên 1 chỗ nhỏ xíu\n\n"
            "Nhiều chị setup xong bếp 4m² mà trông rộng gấp đôi ạ 🏠✨\n\n"
            "Chị muốn em tư vấn bắt đầu từ đâu không?"
        ),
        quick_replies=["🎁 Xem combo", "💰 Xem giá", "📸 Xem hình before/after"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 6: CHÀO HỎI & KẾT THÚC (ưu tiên thấp)
    # ═══════════════════════════════════════════

    # 17. CHÀO HỎI
    Scenario(
        keywords=[
            "chào", "hello", "hi", "alo", "halo", "ơi", "cho hỏi",
            "tư vấn", "xin chào", "chao", "hey",
        ],
        response=(
            "Chào chị! 🏠 Em là Chun — tư vấn viên của Chun Store.\n\n"
            "Chun Store chuyên đồ gia dụng Hàn Quốc giúp bếp gọn đẹp ✨\n\n"
            "Chị đang cần tìm hiểu gì ạ?"
        ),
        quick_replies=["📋 Xem bảng giá", "🛍️ Xem combo", "❓ Tư vấn thêm", "🚚 Thông tin ship"],
    ),

    # 18. CẢM ƠN
    Scenario(
        keywords=[
            "cảm ơn", "cám ơn", "thanks", "tks", "thank", "cam on",
            "cảm ơn nha", "cảm ơn nhé", "ok cảm ơn", "oke cảm ơn",
        ],
        response=(
            "Dạ không có gì ạ! Em cảm ơn chị đã quan tâm Chun Store 🥰\n\n"
            "Chị cần gì cứ nhắn em bất cứ lúc nào nhé!\n"
            "Chúc chị có căn bếp đẹp như ý 🏠✨"
        ),
        quick_replies=["🛒 Đặt hàng", "📋 Xem bảng giá", "🎁 Xem combo"],
    ),

    # 19. TẠM BIỆT
    Scenario(
        keywords=[
            "tạm biệt", "bye", "bb", "bai", "tạm", "goodbye",
            "để sau", "mai tính", "để em suy nghĩ", "suy nghĩ đã",
            "để tính", "xem đã", "coi đã",
        ],
        response=(
            "Dạ vâng ạ! Chị cứ từ từ suy nghĩ nhé 😊\n\n"
            "Khi nào cần, chị nhắn lại đây em hỗ trợ ngay ạ!\n"
            "Chúc chị một ngày vui vẻ 🌸"
        ),
        quick_replies=["📋 Xem bảng giá", "🎁 Xem combo"],
    ),

    # 20. OK / ĐỒNG Ý (nhẹ nhàng chốt)
    Scenario(
        keywords=[
            "ok", "oke", "oki", "okie", "được", "dc", "ờ", "ừ",
            "vâng", "dạ", "đồng ý", "đúng rồi",
        ],
        response=(
            "Dạ chị muốn em hỗ trợ thêm gì ạ? 😊\n\n"
            "Em có thể giúp chị xem giá, tư vấn sản phẩm, hoặc đặt hàng luôn ạ!"
        ),
        quick_replies=["📋 Xem bảng giá", "🛒 Đặt hàng", "🎁 Xem combo", "❓ Tư vấn thêm"],
    ),

    # 21. KHÔNG HIỂU / HỎI LẠI
    Scenario(
        keywords=[
            "không hiểu", "gì", "hả", "sao", "nói lại",
            "em ơi", "nói rõ hơn",
        ],
        response=(
            "Dạ em xin lỗi chị — để em giải thích rõ hơn ạ! 😊\n\n"
            "Chun Store bán 3 sản phẩm gia dụng Hàn Quốc:\n"
            "🧊 Khay tủ lạnh — giữ tủ lạnh gọn gàng\n"
            "🔩 Kệ dán tường — không cần khoan, phù hợp nhà thuê\n"
            "🌀 Hộp xoay gia vị — tiết kiệm diện tích bếp\n\n"
            "Chị muốn tìm hiểu sản phẩm nào ạ?"
        ),
        quick_replies=["📋 Xem bảng giá", "🎁 Xem combo", "🚚 Thông tin ship", "❓ Tư vấn thêm"],
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
    result = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
    return result.lower().strip()


def normalize(text: str) -> str:
    """Chuẩn hóa text để so sánh: bỏ dấu + lowercase + padding."""
    return " " + _no_accent(text) + " "


def _kw_pattern(keyword: str) -> _re.Pattern:
    """
    Tạo regex khớp keyword ở ranh giới từ.
    Dùng (?<!\\w) và (?!\\w) thay vì \\b vì \\b không hiểu Unicode.
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
    msg = normalize(message)
    for scenario in SCENARIOS:
        for keyword in scenario.keywords:
            kw = _no_accent(keyword)
            if len(kw) <= 3:
                pat = _PATTERN_CACHE.setdefault(kw, _kw_pattern(kw))
                if pat.search(msg):
                    return scenario
            else:
                if kw in msg:
                    return scenario
    return None
