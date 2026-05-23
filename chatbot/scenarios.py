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

Tone: Viết như nhân viên THẬT nhắn tin — tự nhiên, không robot.
- Bớt emoji (1-2 cái/tin, KHÔNG rải đều)
- Bớt bullet point, viết liền mạch
- Không phải câu nào cũng "Dạ... ạ"
- Mỗi tin khác tone 1 chút cho không bị lặp
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
            "Okk chị, để em lên đơn nha!\n\n"
            "Chị gửi em mấy thông tin:\n"
            "- Sản phẩm muốn lấy (khay tủ lạnh / kệ dán / hộp xoay / combo)\n"
            "- Tên + SĐT người nhận\n"
            "- Địa chỉ giao hàng\n\n"
            "Em xác nhận đơn rồi báo phí ship cho chị liền ạ"
        ),
        quick_replies=["Muốn mua combo", "Muốn mua khay tủ lạnh", "Muốn mua kệ dán tường"],
    ),

    # 2. MUỐN MUA COMBO
    Scenario(
        keywords=["muốn mua combo", "đặt combo", "lấy combo", "chốt combo", "mua bộ"],
        response=(
            "Chị chọn combo là tiết kiệm nhất luôn á!\n\n"
            "Combo 3 SP giá 419K – 599K, tiết kiệm ~30% so với mua lẻ. "
            "Gồm khay tủ lạnh + kệ dán + hộp xoay, tặng thêm ebook + video hướng dẫn setup. "
            "Đơn từ 499K em freeship luôn nha.\n\n"
            "Chị gửi em tên, SĐT, địa chỉ để em lên đơn nhé!"
        ),
        quick_replies=["Xem bảng giá", "Thông tin ship"],
    ),

    # 3. MUỐN MUA KHAY TỦ LẠNH
    Scenario(
        keywords=["muốn mua khay tủ lạnh", "mua khay", "lấy khay", "đặt khay"],
        response=(
            "Khay tủ lạnh bên em có 3 size nè chị:\n"
            "- Size S (nhỏ): 89K — vừa ngăn nhỏ để trứng, gia vị\n"
            "- Size M (trung): 109K — cái này phổ biến nhất\n"
            "- Size L (lớn): 149K — để rau củ rộng rãi\n\n"
            "Nhựa PP an toàn, chịu lạnh -20°C luôn. "
            "Chị muốn lấy size nào? Gửi em thông tin em lên đơn nha"
        ),
        quick_replies=["Xem combo tiết kiệm hơn", "Phí ship bao nhiêu"],
    ),

    # 4. MUỐN MUA KỆ DÁN TƯỜNG
    Scenario(
        keywords=["muốn mua kệ dán tường", "muốn mua kệ", "mua kệ", "lấy kệ", "đặt kệ"],
        response=(
            "Kệ dán tường có 2 loại nè chị:\n"
            "- 1 tầng: 129K — gọn, để gia vị vừa đẹp\n"
            "- 2 tầng: 199K — để được nhiều hơn\n\n"
            "Inox 304 chống gỉ, dán nano chịu 5kg. "
            "Gỡ ra không hỏng tường luôn nên nhà thuê dùng thoải mái.\n\n"
            "Chị lấy loại nào? Gửi em tên, SĐT, địa chỉ em ship nha"
        ),
        quick_replies=["Xem combo tiết kiệm hơn", "Phí ship bao nhiêu"],
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
            "Giá bên em nè chị:\n\n"
            "Khay tủ lạnh: 89K – 149K\n"
            "Kệ dán tường: 129K – 199K\n"
            "Hộp gia vị xoay: 169K – 249K\n"
            "Combo 3 SP: 419K – 599K (tiết kiệm 30%)\n\n"
            "Mua combo là hời nhất, được tặng thêm ebook + video hướng dẫn setup bếp đẹp nữa. "
            "Chị quan tâm cái nào nhất?"
        ),
        quick_replies=["Xem combo", "Đặt hàng ngay", "Thông tin ship"],
    ),

    # 6. COMBO
    Scenario(
        keywords=["combo", "bộ", "set", "mua combo", "xem combo"],
        response=(
            "Combo 3 SP gồm: Khay tủ lạnh + Kệ dán tường + Hộp gia vị xoay\n\n"
            "Giá 419K – 599K, tiết kiệm ~30% so với mua lẻ. "
            "Tặng kèm ebook \"7 ngày bếp đẹp kiểu Hàn\" + video hướng dẫn setup. "
            "Cả 3 đồng bộ tone trắng/gỗ nên bếp nhìn gọn hẳn.\n\n"
            "Chị muốn đặt combo luôn không?"
        ),
        quick_replies=["Đặt combo ngay", "Phí ship bao nhiêu", "Xem bảng giá"],
    ),

    # 7. KÍCH THƯỚC / SIZE
    Scenario(
        keywords=[
            "kích thước", "size", "kích cỡ", "bao lớn", "bao to",
            "dài bao nhiêu", "rộng bao nhiêu", "cao bao nhiêu",
            "vừa tủ không", "vừa bếp không",
        ],
        response=(
            "Size chi tiết nè chị:\n\n"
            "Khay tủ lạnh: S 15×10×6cm / M 25×15×8cm / L 32×20×10cm\n"
            "Kệ dán: 1 tầng 40×12×10cm / 2 tầng 40×12×25cm\n"
            "Hộp xoay: đường kính 25cm, cao 20cm\n\n"
            "Chị cho em biết tủ lạnh/bếp rộng cỡ nào em tư vấn size phù hợp nha"
        ),
        quick_replies=["Xem giá", "Đặt hàng", "Tư vấn thêm"],
    ),

    # 8. CHẤT LIỆU / NGUỒN GỐC
    Scenario(
        keywords=[
            "chất liệu", "nguyên liệu", "nhựa", "inox", "an toàn",
            "hàn quốc", "xuất xứ", "nguồn gốc", "chính hãng",
            "có độc không", "bpa", "chat lieu",
        ],
        response=(
            "Hàng bên em nhập Hàn Quốc nha chị, có kiểm định chất lượng.\n\n"
            "Khay tủ lạnh bằng nhựa PP, không BPA, chịu được -20°C đến 120°C. "
            "Kệ dán bằng inox 304 không gỉ + keo nano chịu 5kg. "
            "Hộp gia vị bằng nhựa ABS + PP bền, chống va đập.\n\n"
            "Chị yên tâm dùng nha, an toàn thực phẩm luôn"
        ),
        quick_replies=["Xem giá", "Đặt hàng", "Thông tin ship"],
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
            "Hình thực tế + review chị qua page Chun Store xem nha, nhiều before/after lắm!\n\n"
            "Mấy chị mua rồi feedback:\n"
            "- \"Tủ lạnh gọn hẳn, mở ra sướng mắt\" — chị Linh ở HN\n"
            "- \"Bếp nhà thuê mà trông xịn như phim Hàn\" — chị Nga ở SG\n\n"
            "Đổi trả 7 ngày nếu không ưng nha chị, cứ thử thoải mái"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Chính sách đổi trả"],
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
            "Ship COD toàn quốc nha chị — nhận hàng rồi mới trả tiền.\n\n"
            "Phí ship 25K – 35K tùy khu vực. Đơn từ 499K em freeship luôn.\n"
            "HN/HCM giao 1-2 ngày, tỉnh thì 2-5 ngày.\n\n"
            "Chị ở đâu để em báo chính xác phí ship nha?"
        ),
        quick_replies=["Đặt hàng", "Xem combo freeship", "Xem bảng giá"],
    ),

    # 11. ĐỔI TRẢ / BẢO HÀNH
    Scenario(
        keywords=[
            "đổi trả", "hoàn tiền", "trả hàng", "bảo hành", "chính sách",
            "lỗi", "hỏng", "không giống hình", "đổi", "trả",
            "doi tra", "bao hanh", "chinh sach",
        ],
        response=(
            "Bên em đổi trả trong 7 ngày nha chị.\n\n"
            "Nếu hàng lỗi, không đúng mô tả, hay giao nhầm — chị quay video lúc unbox rồi nhắn em. "
            "Em đổi/hoàn trong 1-2 ngày luôn.\n\n"
            "Cam kết hàng đúng hình, đúng chất lượng. Chị cứ yên tâm đặt nha"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Hỏi thêm"],
    ),

    # 12. NHÀ THUÊ / KHÔNG KHOAN
    Scenario(
        keywords=[
            "nhà thuê", "thuê nhà", "không khoan", "không được khoan",
            "dán", "dán tường", "trả phòng", "tiền cọc", "nha thue",
            "khoan tường", "sợ hỏng tường",
        ],
        response=(
            "Nhà thuê thì dùng kệ dán bên em hợp lắm chị!\n\n"
            "Keo nano dán chắc chịu 5kg, mà gỡ ra sạch không để vết. "
            "Trả phòng không sợ mất cọc. Inox 304 nên dầu mỡ, nước cũng không sao.\n\n"
            "Nhiều chị thuê nhà dùng xong tiếc sao không mua sớm hơn luôn á"
        ),
        quick_replies=["Xem giá kệ dán", "Đặt hàng", "Xem combo"],
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
            "Hiện tại mua combo là deal tốt nhất luôn chị:\n\n"
            "Combo 3 SP tiết kiệm 30% so với mua lẻ, freeship cho đơn từ 499K, "
            "tặng thêm ebook + video hướng dẫn setup.\n\n"
            "Chị muốn em gửi thông tin combo không?"
        ),
        quick_replies=["Xem combo", "Xem bảng giá", "Đặt hàng"],
    ),

    # 14. SO SÁNH / TỐT HƠN GÌ
    Scenario(
        keywords=[
            "so sánh", "khác gì", "hơn gì", "tốt hơn", "shopee",
            "lazada", "tiki", "ngoài chợ", "ngoài tiệm",
            "mua ở đâu rẻ hơn", "bên khác", "hàng tàu",
        ],
        response=(
            "Thật ra Shopee/chợ có hàng rẻ hơn 20-30K thật, nhưng nhựa mỏng dễ vỡ, "
            "không rõ nguồn gốc, mà không đổi trả được.\n\n"
            "Bên em hàng nhập Hàn Quốc, nhựa PP an toàn thực phẩm. "
            "Được đổi trả 7 ngày, em còn chăm sóc 7 ngày sau mua nữa. "
            "Chênh vài chục K thôi mà dùng an tâm hơn nhiều chị ạ"
        ),
        quick_replies=["Xem combo", "Đặt hàng", "Xem bảng giá"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 5: XỬ LÝ TỪ CHỐI (Chris Voss — Straight Line)
    # ═══════════════════════════════════════════

    # 15. "ĐẮT QUÁ"
    Scenario(
        keywords=[
            "đắt quá", "mắc quá", "đắt", "mắc", "giá cao", "chát",
            "đắt vậy", "mắc vậy", "sao đắt", "giá cao quá",
            "dat qua", "mac qua", "nhieu tien qua",
        ],
        response=(
            "Em hiểu chị, nhìn giá thấy ngại thiệt.\n\n"
            "Nhưng chị tính coi — hàng chợ 50-70K dùng 2-3 tháng hỏng, phải mua lại. "
            "Bên em 89-149K dùng 2-3 năm, an toàn thực phẩm. Tính ra rẻ hơn nhiều.\n\n"
            "Mà nếu chị lấy combo 3 SP chỉ 419K, tiết kiệm 30% + freeship luôn á"
        ),
        quick_replies=["Xem combo tiết kiệm", "Xem bảng giá", "Xem review KH"],
    ),

    # 16. "ĐỂ SUY NGHĨ"
    Scenario(
        keywords=[
            "suy nghĩ", "để suy nghĩ", "tính đã", "xem đã", "coi đã",
            "để tính", "nghĩ đã", "chưa quyết", "phân vân",
            "suy nghi", "chua quyet",
        ],
        response=(
            "Dạ chị cứ từ từ nha, không vội!\n\n"
            "Mà em hỏi thiệt — chị đang phân vân chỗ nào? "
            "Giá cả, chất lượng, hay chưa biết chọn gì? "
            "Nói em biết em tư vấn đúng hơn cho chị"
        ),
        quick_replies=["Lo về giá", "Lo về chất lượng", "Chưa biết chọn gì"],
    ),

    # 17. "SHOPEE RẺ HƠN"
    Scenario(
        keywords=[
            "shopee rẻ hơn", "lazada rẻ hơn", "mua shopee", "trên shopee",
            "bên kia rẻ hơn", "chỗ khác rẻ hơn", "rẻ hơn",
        ],
        response=(
            "Ừa Shopee có hàng rẻ hơn thật chị. Em không phủ nhận.\n\n"
            "Nhưng mua bên em chị được thêm: hàng Hàn Quốc chính hãng không lo BPA, "
            "đổi trả 7 ngày không ưng hoàn tiền, em chăm sóc 7 ngày sau mua, "
            "tặng video setup + ebook bếp đẹp.\n\n"
            "Chênh vài chục K thôi mà an tâm hơn nhiều. Chị muốn xem combo không?"
        ),
        quick_replies=["Xem combo", "Xem review KH", "Đặt hàng"],
    ),

    # 18. "HỎI CHỒNG"
    Scenario(
        keywords=[
            "hỏi chồng", "hỏi vợ", "hỏi ông xã", "bàn với chồng",
            "bàn với vợ", "để hỏi", "hỏi gia đình",
        ],
        response=(
            "Dạ chị cứ bàn với anh nhà!\n\n"
            "Em gửi tóm tắt cho chồng xem nhanh nha: "
            "Combo 3 SP đồ gia dụng Hàn Quốc giá 419K, freeship, COD nhận hàng mới trả tiền, "
            "đổi trả 7 ngày không ưng hoàn lại.\n\n"
            "Khi nào anh chị quyết rồi nhắn em, em lên đơn liền nha"
        ),
        quick_replies=["Đặt hàng", "Xem bảng giá", "Xem combo"],
    ),

    # 19. "HẾT TIỀN"
    Scenario(
        keywords=[
            "hết tiền", "không có tiền", "chưa có tiền", "tiền không đủ",
            "eo hẹp", "lương chưa về", "cuối tháng",
            "het tien", "khong co tien",
        ],
        response=(
            "Dạ em hiểu chị! Không cần mua combo ngay đâu.\n\n"
            "Chị mua lẻ 1 cái trước cũng được — khay tủ lạnh chỉ 89K thôi, "
            "mà tủ lạnh gọn hẳn luôn. Dùng thấy ok rồi mua thêm sau cũng được.\n\n"
            "Ship COD nên chị nhận hàng rồi mới trả tiền, không cần CK trước nha"
        ),
        quick_replies=["Xem khay 89K", "Xem kệ 129K", "Xem bảng giá"],
    ),

    # 20. "CHƯA CẦN"
    Scenario(
        keywords=[
            "chưa cần", "không cần", "chưa muốn mua", "không muốn",
            "thôi", "không mua", "thôi khỏi", "ko cần", "k cần",
            "chua can", "khong can",
        ],
        response=(
            "Ok chị, không sao!\n\n"
            "Khi nào cần chị cứ nhắn em nha. "
            "Nhiều chị bắt đầu bằng 1 khay tủ lạnh 89K thôi, dùng thấy thích rồi mua thêm dần. "
            "Không cần mua hết 1 lúc đâu ạ.\n\n"
            "Chúc chị ngày vui!"
        ),
        quick_replies=["Xem bảng giá", "Xem combo", "Xem hình thực tế"],
    ),

    # 21. "ĐÃ CÓ RỒI"
    Scenario(
        keywords=[
            "có rồi", "mua rồi", "đã có", "dùng rồi", "xài rồi",
            "có hết rồi", "co roi", "da co",
        ],
        response=(
            "Ồ chị có rồi á? Dùng hãng nào vậy chị?\n\n"
            "Nếu thấy nhựa bắt đầu ố vàng hay kệ dán bong thì nên đổi qua nhựa PP Hàn bền hơn nè. "
            "Hoặc chị mua tặng bạn bè người thân cũng hay — "
            "nhiều chị mua xong còn mua thêm tặng mẹ nữa á"
        ),
        quick_replies=["Xem combo tặng", "Xem giá", "Xem hình"],
    ),

    # 22. "KHÔNG TIN"
    Scenario(
        keywords=[
            "không tin", "lừa đảo", "scam", "giả", "sợ lừa",
            "có thật không", "có uy tín không", "tin được không",
            "co that khong", "lua dao",
        ],
        response=(
            "Chị lo mua online bị lừa em hiểu chị.\n\n"
            "Bên em ship COD — chị nhận hàng kiểm tra rồi mới trả tiền, không rủi ro gì hết. "
            "Đổi trả 7 ngày, chị quay video lúc mở hàng, có vấn đề em đổi ngay.\n\n"
            "Feedback khách: \"Hàng y hình, đóng gói cẩn thận\" — chị Linh ở HN. "
            "Chị cứ thử đặt 1 cái, không ưng em hoàn tiền nha"
        ),
        quick_replies=["Đặt hàng COD", "Xem thêm review", "Xem giá"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 6: SẢN PHẨM CHI TIẾT & SỬ DỤNG
    # ═══════════════════════════════════════════

    # 23. CÒN HÀNG KHÔNG / HẾT HÀNG
    Scenario(
        keywords=[
            "còn hàng", "hết hàng", "còn không", "có hàng không", "có sẵn",
            "con hang", "het hang", "con ko", "con k", "stocking",
            "bao giờ có hàng", "khi nào có", "hàng về chưa",
        ],
        response=(
            "Hàng bên em có sẵn luôn chị, đặt là ship liền.\n\n"
            "Chị muốn lấy gì em lên đơn nha?"
        ),
        quick_replies=["Xem bảng giá", "Đặt hàng", "Xem combo"],
    ),

    # 24. MÀU SẮC
    Scenario(
        keywords=[
            "màu", "màu gì", "có màu", "màu trắng", "màu gỗ",
            "mau gi", "co mau", "color", "tone",
        ],
        response=(
            "Bên em có tone trắng và tone gỗ nha chị. "
            "Cả 2 đều minimalist kiểu Hàn, phối với bếp nào cũng hợp.\n\n"
            "Mua combo thì 3 cái đồng bộ 1 tone luôn, bếp nhìn gọn hẳn. "
            "Chị thích tone nào?"
        ),
        quick_replies=["Xem combo", "Xem hình thực tế", "Đặt hàng"],
    ),

    # 25. CÁCH SỬ DỤNG / LẮP ĐẶT
    Scenario(
        keywords=[
            "cách dùng", "sử dụng", "lắp đặt", "lắp", "setup",
            "cách lắp", "hướng dẫn", "dùng sao", "dùng thế nào",
            "cach dung", "lap dat", "huong dan", "dung nhu the nao",
            "cách sử dụng", "khó lắp không", "dễ dùng không",
        ],
        response=(
            "Dễ lắm chị, không cần thợ đâu!\n\n"
            "Khay tủ lạnh bỏ vào tủ là xong. "
            "Kệ dán tường lau sạch tường → dán lên → chờ 24h rồi treo đồ. "
            "Hộp xoay đặt lên bàn bếp xoay 360 độ luôn.\n\n"
            "Mua combo em tặng kèm video hướng dẫn setup chi tiết nha"
        ),
        quick_replies=["Xem combo", "Đặt hàng", "Xem giá"],
    ),

    # 26. VỆ SINH / RỬA
    Scenario(
        keywords=[
            "rửa", "vệ sinh", "lau", "dọn", "bẩn", "ố",
            "rua", "ve sinh", "co kho rua", "dễ rửa",
            "rửa bằng gì", "có dễ vệ sinh", "lau chùi",
        ],
        response=(
            "Rửa bình thường bằng nước rửa chén là sạch nha chị.\n\n"
            "Khay nhựa PP trơn nhẵn không bám dầu mỡ. "
            "Kệ inox thì lau khăn ướt là sáng bóng lại. "
            "Chị không cần lo vệ sinh đâu, dễ lắm"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Xem hình"],
    ),

    # 27. BỀN KHÔNG / DÙNG BAO LÂU
    Scenario(
        keywords=[
            "bền không", "dùng được bao lâu", "tuổi thọ", "lâu không",
            "mấy năm", "bao lâu hỏng", "có bền", "ben khong",
            "dung duoc bao lau", "xài bao lâu", "bao lau hong",
        ],
        response=(
            "Dùng 2-3 năm bình thường chị, giữ kỹ thì lâu hơn.\n\n"
            "Nhựa PP Hàn dày hơn hàng chợ nên không dễ nứt vỡ. "
            "Kệ inox 304 thì không gỉ, dùng mấy năm vẫn sáng. "
            "So với hàng chợ 2-3 tháng hỏng thì khác biệt lớn lắm"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Xem combo"],
    ),

    # 28. THANH TOÁN
    Scenario(
        keywords=[
            "thanh toán", "trả tiền", "chuyển khoản", "ck", "momo",
            "banking", "chuyển tiền", "trả trước", "thanh toan",
            "chuyen khoan", "tra tien", "payment",
        ],
        response=(
            "Bên em ship COD nha chị — nhận hàng kiểm tra rồi mới trả tiền, "
            "không cần chuyển khoản trước.\n\n"
            "An toàn, không rủi ro gì hết. Chị muốn đặt luôn không?"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Xem combo"],
    ),

    # 29. MUA SỈ / SỐ LƯỢNG NHIỀU
    Scenario(
        keywords=[
            "mua sỉ", "sỉ", "số lượng lớn", "nhiều cái", "mua nhiều",
            "bán sỉ", "giá sỉ", "wholesale", "mua si", "ban si",
            "10 cái", "20 cái", "50 cái", "100 cái",
        ],
        response=(
            "Chị muốn lấy số lượng nhiều á? Được chị!\n\n"
            "Chị cho em biết cần SP gì, bao nhiêu cái, em báo giá sỉ riêng cho chị nha. "
            "Lấy nhiều em có giá tốt hơn"
        ),
        quick_replies=["Xem bảng giá lẻ", "Đặt hàng"],
    ),

    # 30. TRACKING ĐƠN / ĐƠN HÀNG ĐÂU
    Scenario(
        keywords=[
            "đơn hàng", "tracking", "đơn đâu", "hàng đâu", "đơn của tôi",
            "kiểm tra đơn", "theo dõi đơn", "don hang", "hang dau",
            "bao giờ giao", "giao chưa", "ship chưa", "đã giao chưa",
            "em ơi đơn", "mã đơn", "mã vận đơn",
        ],
        response=(
            "Chị cho em SĐT hoặc tên người nhận đơn để em tra nha!\n\n"
            "Thường HN/HCM 1-2 ngày, tỉnh 2-5 ngày. "
            "Em kiểm tra xong báo chị liền"
        ),
        quick_replies=["Hỏi thêm"],
    ),

    # 31. HỦY ĐƠN / ĐỔI ĐƠN
    Scenario(
        keywords=[
            "hủy đơn", "hủy", "cancel", "đổi đơn", "sửa đơn",
            "đổi địa chỉ", "đổi sdt", "đổi size", "đổi sản phẩm",
            "huy don", "doi don", "sua don",
        ],
        response=(
            "Chị muốn hủy/sửa đơn hả? Được chị!\n\n"
            "Chị cho em biết tên + SĐT đặt đơn, và muốn sửa gì, em xử lý nha. "
            "Nếu hàng chưa giao thì sửa được liền"
        ),
        quick_replies=["Hỏi thêm"],
    ),

    # 32. MUA TẶNG
    Scenario(
        keywords=[
            "tặng", "quà tặng", "mua tặng", "tặng bạn", "tặng mẹ",
            "tặng chị", "tặng vợ", "quà", "gift", "mua tang",
            "tặng sinh nhật", "tặng tân gia", "quà tân gia",
        ],
        response=(
            "Mua tặng thì combo là hợp nhất luôn chị!\n\n"
            "Combo 3 SP đồng bộ tone trắng/gỗ, đóng hộp đẹp. "
            "Tặng tân gia, sinh nhật, hay cho mẹ đều ý nghĩa. "
            "Nhiều chị mua xong còn quay lại mua thêm tặng người quen nữa.\n\n"
            "Chị muốn ship đến địa chỉ người nhận luôn không?"
        ),
        quick_replies=["Đặt combo tặng", "Xem giá", "Xem hình"],
    ),

    # 33. CÓ SHOP OFFLINE KHÔNG
    Scenario(
        keywords=[
            "shop ở đâu", "cửa hàng", "showroom", "mua trực tiếp",
            "shop o dau", "cua hang", "địa chỉ shop", "ghé shop",
            "có shop không", "mua tại chỗ",
        ],
        response=(
            "Bên em bán online thôi chị, chưa có shop offline.\n\n"
            "Nhưng chị yên tâm — ship COD nhận hàng mới trả tiền, "
            "đổi trả 7 ngày nếu không ưng. Không rủi ro gì hết nha"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Xem review"],
    ),

    # 34. EBOOK / VIDEO TẶNG
    Scenario(
        keywords=[
            "ebook", "video", "hướng dẫn setup", "sách", "tài liệu",
            "7 ngày bếp đẹp", "bếp đẹp kiểu hàn",
        ],
        response=(
            "Mua combo em tặng kèm 2 thứ:\n"
            "- Ebook \"7 ngày bếp đẹp kiểu Hàn\" — hướng dẫn setup từng ngày\n"
            "- Video hướng dẫn lắp đặt + sắp xếp chi tiết\n\n"
            "Nhiều chị làm theo xong bếp thay đổi hẳn luôn á. "
            "Chị muốn xem combo không?"
        ),
        quick_replies=["Xem combo", "Đặt hàng", "Xem giá"],
    ),

    # 35. NẶNG BAO NHIÊU / CÂN NẶNG
    Scenario(
        keywords=[
            "nặng", "cân nặng", "bao nặng", "kg", "gram",
            "nang bao nhieu", "nặng không",
        ],
        response=(
            "Nhẹ lắm chị, khay tủ lạnh khoảng 200-400g tùy size. "
            "Kệ dán tường 500g-1kg. Hộp xoay khoảng 800g.\n\n"
            "Combo gộp lại cũng chỉ ~2kg thôi. Chị cần biết thêm gì không?"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Xem size"],
    ),

    # 36. GIAO CUỐI TUẦN / GIAO GIỜ NÀO
    Scenario(
        keywords=[
            "giao cuối tuần", "giao thứ 7", "giao chủ nhật",
            "giao giờ nào", "giao buổi tối", "giao sáng",
            "giao t7", "giao cn", "ngày nghỉ",
        ],
        response=(
            "Bên vận chuyển giao T2-T7 nha chị, CN nghỉ. "
            "Giờ giao thường 8h-18h, shipper sẽ gọi trước khi giao.\n\n"
            "Chị muốn đặt em lên đơn nha?"
        ),
        quick_replies=["Đặt hàng", "Xem giá"],
    ),

    # 37. ĐÓNG GÓI
    Scenario(
        keywords=[
            "đóng gói", "gói", "bọc", "bubble", "hộp",
            "dong goi", "đóng hộp", "có đóng gói kỹ không",
            "giao có bể không", "vỡ không",
        ],
        response=(
            "Em đóng gói cẩn thận nha chị — bọc bubble wrap + hộp carton, "
            "không lo bể vỡ khi vận chuyển.\n\n"
            "Lỡ nhận hàng có vấn đề chị quay video rồi nhắn em, em đổi ngay"
        ),
        quick_replies=["Đặt hàng", "Xem giá", "Chính sách đổi trả"],
    ),

    # 38. KHIẾU NẠI / KHÔNG HÀI LÒNG
    Scenario(
        keywords=[
            "khiếu nại", "complain", "không hài lòng", "tệ", "dở",
            "thất vọng", "kém", "thua", "khong hai long",
            "chất lượng kém", "không như hình", "khác hình",
        ],
        response=(
            "Ôi chị ơi, em xin lỗi nếu có gì không ưng ạ!\n\n"
            "Chị gửi em hình/video sản phẩm + mô tả vấn đề, "
            "em xử lý đổi/hoàn cho chị trong 1-2 ngày nha. "
            "Cam kết chị hài lòng mới thôi"
        ),
        quick_replies=["Chính sách đổi trả", "Liên hệ hotline"],
    ),

    # 39. GỬI ĐỊA CHỈ / THÔNG TIN ĐẶT HÀNG
    Scenario(
        keywords=[
            "địa chỉ của em", "địa chỉ mình", "gửi địa chỉ",
            "mình ở", "em ở", "chị ở", "nhà mình ở",
            "quận", "huyện", "phường", "tỉnh", "thành phố",
        ],
        response=(
            "Ok chị, em nhận địa chỉ rồi!\n\n"
            "Chị cho em thêm tên + SĐT người nhận, "
            "và chị muốn lấy SP gì để em lên đơn nha"
        ),
        quick_replies=["Xem bảng giá", "Xem combo", "Đặt hàng"],
    ),

    # 40. HỎI VỀ GROUP / CỘNG ĐỒNG
    Scenario(
        keywords=[
            "group", "nhóm", "cộng đồng", "community", "facebook group",
            "bếp hàn việt", "tham gia", "vào nhóm",
        ],
        response=(
            "Bên em có group \"Bếp Hàn Việt\" trên Facebook nha chị! "
            "Mọi người chia sẻ before/after, tips sắp xếp bếp, review sản phẩm.\n\n"
            "Mua hàng xong em add chị vào group luôn. "
            "Nhiều ý tưởng setup bếp hay lắm"
        ),
        quick_replies=["Đặt hàng", "Xem combo", "Xem hình"],
    ),

    # 41. CHUN STORE LÀ GÌ / BÁN GÌ
    Scenario(
        keywords=[
            "bán gì", "chun store là gì", "shop bán gì", "bán cái gì",
            "ban gi", "là shop gì", "giới thiệu",
        ],
        response=(
            "Chun Store chuyên đồ gia dụng Hàn Quốc giúp bếp gọn đẹp nha chị!\n\n"
            "Bên em có 3 sản phẩm chính: "
            "khay tổ chức tủ lạnh, kệ gia vị dán tường không khoan, "
            "và hộp gia vị xoay 360°.\n\n"
            "Chị đang cần gì để em tư vấn?"
        ),
        quick_replies=["Xem bảng giá", "Xem combo", "Xem hình"],
    ),

    # 42. NHẮN LẠI SAU / BẬN
    Scenario(
        keywords=[
            "nhắn lại sau", "bận", "đang bận", "lát nữa", "tí nữa",
            "chút nữa", "nhan lai sau", "dang ban", "lát nhắn lại",
            "mai nhắn", "tối nhắn",
        ],
        response=(
            "Ok chị, cứ từ từ! Khi nào rảnh nhắn em nha, em online 8h-21h hàng ngày"
        ),
        quick_replies=["Xem bảng giá", "Xem combo"],
    ),

    # 43. GỬI HÌNH BẾP / TỦ LẠNH
    Scenario(
        keywords=[
            "gửi hình bếp", "bếp nhà em", "tủ lạnh nhà em",
            "nhà em", "bếp em", "xem bếp", "gửi ảnh bếp",
        ],
        response=(
            "Chị gửi hình bếp/tủ lạnh nhà chị đi, em xem rồi tư vấn SP phù hợp nha!\n\n"
            "Biết size bếp + style chị thích thì em recommend chính xác hơn"
        ),
        quick_replies=["Xem combo", "Xem giá", "Xem hình before/after"],
    ),

    # 44. HỎI VỀ CSKH SAU MUA
    Scenario(
        keywords=[
            "sau mua", "sau khi mua", "hậu mãi", "chăm sóc",
            "cskh", "customer service", "hỗ trợ sau mua",
        ],
        response=(
            "Sau khi mua em chăm sóc 7 ngày liền nha chị:\n"
            "- Ngày 1: hỏi chị nhận hàng ổn không\n"
            "- Ngày 3: hỏi dùng có ok không, cần hỗ trợ gì\n"
            "- Ngày 7: hỏi feedback, mời vào group Bếp Hàn Việt\n\n"
            "Có vấn đề gì chị nhắn em bất cứ lúc nào"
        ),
        quick_replies=["Đặt hàng", "Xem combo", "Xem giá"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 7: LIÊN HỆ & HỖ TRỢ
    # ═══════════════════════════════════════════

    # 45. SĐT / HOTLINE
    Scenario(
        keywords=[
            "sdt", "số điện thoại", "hotline", "liên hệ", "gọi",
            "phone", "zalo", "so dien thoai", "lien he", "gọi cho ai",
            "sđt", "điện thoại",
        ],
        response=(
            "Chị liên hệ em qua:\n"
            "- Nhắn tin ngay đây (nhanh nhất)\n"
            "- Zalo: 0xxx.xxx.xxx\n\n"
            "Em hỗ trợ 8h – 21h hàng ngày nha chị"
        ),
        quick_replies=["Xem giá", "Đặt hàng", "Hỏi thêm"],
    ),

    # 46. BẾP NHỎ / BẾP BỪA
    Scenario(
        keywords=[
            "bếp nhỏ", "bếp chật", "bếp bừa", "bừa bộn", "ngán",
            "tủ lạnh bừa", "đồ ngập", "không có chỗ", "hết chỗ",
            "bep nho", "bep bua", "tu lanh bua",
        ],
        response=(
            "Bếp nhỏ mà đồ cứ ngập lên em hiểu chị lắm!\n\n"
            "Khay tủ lạnh phân chia ngăn gọn, nhìn vào biết có gì. "
            "Kệ dán tường tận dụng chỗ trống, không chiếm mặt bàn. "
            "Hộp xoay để 8-12 ngăn trên 1 chỗ nhỏ xíu.\n\n"
            "Nhiều chị setup xong bếp 4m² mà trông rộng gấp đôi luôn. "
            "Chị muốn em tư vấn bắt đầu từ đâu không?"
        ),
        quick_replies=["Xem combo", "Xem giá", "Xem hình before/after"],
    ),

    # ═══════════════════════════════════════════
    # NHÓM 8: CHÀO HỎI & KẾT THÚC (ưu tiên thấp)
    # ═══════════════════════════════════════════

    # 47. CHÀO HỎI
    Scenario(
        keywords=[
            "chào", "hello", "hi", "alo", "halo", "ơi", "cho hỏi",
            "tư vấn", "xin chào", "chao", "hey",
        ],
        response=(
            "Chào chị! Em là Chun bên Chun Store nè.\n\n"
            "Bên em chuyên đồ gia dụng Hàn Quốc giúp bếp gọn đẹp. "
            "Chị đang tìm hiểu gì để em tư vấn nha?"
        ),
        quick_replies=["Xem bảng giá", "Xem combo", "Tư vấn thêm", "Thông tin ship"],
    ),

    # 48. CẢM ƠN
    Scenario(
        keywords=[
            "cảm ơn", "cám ơn", "thanks", "tks", "thank", "cam on",
            "cảm ơn nha", "cảm ơn nhé", "ok cảm ơn", "oke cảm ơn",
        ],
        response=(
            "Dạ không có gì chị! Cảm ơn chị đã quan tâm Chun Store nha.\n\n"
            "Khi nào cần gì cứ nhắn em. Chúc chị có căn bếp thật đẹp!"
        ),
        quick_replies=["Đặt hàng", "Xem bảng giá", "Xem combo"],
    ),

    # 49. TẠM BIỆT
    Scenario(
        keywords=[
            "tạm biệt", "bye", "bb", "bai", "tạm", "goodbye",
            "để sau", "mai tính",
        ],
        response=(
            "Dạ chị! Khi nào cần cứ nhắn em nha.\n"
            "Chúc chị ngày vui vẻ!"
        ),
        quick_replies=["Xem bảng giá", "Xem combo"],
    ),

    # 50. OK / ĐỒNG Ý
    Scenario(
        keywords=[
            "ok", "oke", "oki", "okie", "được", "dc", "ờ", "ừ",
            "vâng", "dạ", "đồng ý", "đúng rồi",
        ],
        response=(
            "Chị muốn em hỗ trợ thêm gì không? "
            "Em có thể tư vấn sản phẩm, báo giá, hoặc lên đơn cho chị luôn nha"
        ),
        quick_replies=["Xem bảng giá", "Đặt hàng", "Xem combo", "Tư vấn thêm"],
    ),

    # 51. KHÔNG HIỂU / HỎI LẠI
    Scenario(
        keywords=[
            "không hiểu", "gì", "hả", "sao", "nói lại",
            "em ơi", "nói rõ hơn",
        ],
        response=(
            "Sorry chị, để em nói rõ hơn nha!\n\n"
            "Chun Store bán 3 sản phẩm gia dụng Hàn Quốc:\n"
            "- Khay tủ lạnh — giữ tủ lạnh gọn gàng\n"
            "- Kệ dán tường — không cần khoan, nhà thuê dùng ok\n"
            "- Hộp xoay gia vị — tiết kiệm diện tích bếp\n\n"
            "Chị muốn tìm hiểu cái nào?"
        ),
        quick_replies=["Xem bảng giá", "Xem combo", "Thông tin ship", "Tư vấn thêm"],
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
