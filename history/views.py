import uuid
import urllib.parse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count
from .models import Dynasty, Question, Book, Order

def home(request):
    return render(request, 'home.html')

def video_page(request):
    videos = [
        {"title": "Lịch sử Việt Nam tổng hợp", "url": "https://www.youtube.com/embed/RjCWU2RDEh4"},
        {"title": "Kháng chiến chống Pháp", "url": "https://www.youtube.com/embed/AbRg5rH6fxo"},
        {"title": "Kháng chiến chống Mỹ", "url": "https://www.youtube.com/embed/TQehUlbyp3o"}
    ]
    return render(request, 'video.html', {'videos': videos})
# 1. Trang học tập (Lấy dữ liệu từ DB)
def question_page(request):
    dynasties = Dynasty.objects.prefetch_related('questions').all()
    return render(request, 'question.html', {'dynasties': dynasties})

# 2. Trang cửa hàng sách
def book_store(request):
    books = Book.objects.all()  # Hoặc lọc theo điều kiện
    return render(request, 'store.html', {'books': books})

# 3. View tạo QR thanh toán
def initiate_payment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    order_code = str(uuid.uuid4())[:8].upper()
    
    # Tạo đơn hàng tạm thời (Lưu email demo)
    order = Order.objects.create(
        book=book, 
        order_code=order_code, 
        customer_email="nguoimua@gmail.com" # Trong thực tế lấy từ Form
    )
    
    # VietQR config
    BANK_ID = "vcb"
    ACCOUNT_NO = "123456789"
    DESCRIPTION = f"THANH TOAN {order_code}"
    qr_url = f"https://img.vietqr.io/image/{BANK_ID}-{ACCOUNT_NO}-compact2.png?amount={book.price}&addInfo={urllib.parse.quote(DESCRIPTION)}"
    
    return render(request, 'payment.html', {'order': order, 'qr_url': qr_url})

# 4. Xác nhận thanh toán & Gửi Email
def verify_payment_mock(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    order.status = True
    order.save()

    # Logic gửi Email
    subject = f"Xác nhận thanh toán đơn hàng {order.order_code}"
    message = f"Cảm ơn bạn đã mua sách {order.book.title}. Đơn hàng {order.book.price}đ đã thành công."
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [order.customer_email])
    except:
        pass

    return render(request, 'payment_success.html', {'order': order})

# 5. Thống kê (Dùng cho biểu đồ)
def statistics_view(request):
    data = Dynasty.objects.annotate(q_count=Count('questions')).values('name', 'q_count')
    labels = [x['name'] for x in data]
    values = [x['q_count'] for x in data]
    return render(request, 'stats.html', {'labels': labels, 'values': values})

def question_page(request):
    # Dữ liệu 100+ câu hỏi chia theo triều đại / giai đoạn
    data = {
        "NHÀ NGÔ": [
            {"q": "Người sáng lập nhà Ngô là ai?", "options": ["Ngô Quyền", "Đinh Bộ Lĩnh", "Lê Hoàn", "Lý Công Uẩn"], "answer": "Ngô Quyền"},
            {"q": "Nhà Ngô được thành lập năm nào?", "options": ["938", "939", "968", "1009"], "answer": "939"},
            {"q": "Sự kiện nào mở đầu cho nhà Ngô?", "options": ["Chiến thắng Chi Lăng", "Chiến thắng Bạch Đằng (938)", "Chiến thắng Điện Biên Phủ", "Khởi nghĩa Lam Sơn"], "answer": "Chiến thắng Bạch Đằng (938)"},
            {"q": "Kinh đô của nhà Ngô đặt ở đâu?", "options": ["Hoa Lư", "Cổ Loa", "Thăng Long", "Phú Xuân"], "answer": "Cổ Loa"},
            {"q": "Ngô Quyền mất năm nào?", "options": ["944", "939", "950", "965"], "answer": "944"},
            {"q": "Sau khi Ngô Quyền mất, đất nước rơi vào tình trạng gì?", "options": ["Loạn 12 sứ quân", "Bắc thuộc lần 4", "Chiến tranh Nam - Bắc triều", "Trịnh - Nguyễn phân tranh"], "answer": "Loạn 12 sứ quân"},
            {"q": "Ai là con trai của Ngô Quyền?", "options": ["Ngô Xương Ngập", "Ngô Xương Văn", "Cả hai", "Không có con trai"], "answer": "Cả hai"},
            {"q": "Ngô Xương Văn còn được gọi là gì?", "options": ["Hậu Ngô Vương", "Tiền Ngô Vương", "Nam Tấn Vương", "Thiên Sách Vương"], "answer": "Hậu Ngô Vương"},
            {"q": "Ngô Quyền sử dụng chiến thuật gì để đánh quân Nam Hán?", "options": ["Đóng cọc trên sông", "Hỏa công", "Phục binh", "Vây thành"], "answer": "Đóng cọc trên sông"},
            {"q": "Nhà Ngô tồn tại bao nhiêu năm?", "options": ["26", "36", "46", "56"], "answer": "26"},
        ],
        "NHÀ ĐINH": [
            {"q": "Người sáng lập nhà Đinh là ai?", "options": ["Lê Hoàn", "Ngô Quyền", "Đinh Bộ Lĩnh", "Lý Công Uẩn"], "answer": "Đinh Bộ Lĩnh"},
            {"q": "Đinh Bộ Lĩnh lên ngôi vua năm nào?", "options": ["939", "968", "1009", "1010"], "answer": "968"},
            {"q": "Kinh đô Hoa Lư thuộc tỉnh nào ngày nay?", "options": ["Ninh Bình", "Thanh Hóa", "Hà Nội", "Hà Nam"], "answer": "Ninh Bình"},
            {"q": "Đinh Bộ Lĩnh đặt tên nước là gì?", "options": ["Đại Cồ Việt", "Đại Việt", "Vạn Xuân", "Đại Nam"], "answer": "Đại Cồ Việt"},
            {"q": "Đinh Bộ Lĩnh bị ám sát năm nào?", "options": ["979", "968", "981", "1009"], "answer": "979"},
            {"q": "Ai là người kế vị sau khi Đinh Tiên Hoàng bị sát hại?", "options": ["Đinh Liễn", "Đinh Toàn", "Lê Hoàn", "Đinh Hạng Lang"], "answer": "Đinh Toàn"},
            {"q": "Thái hậu Dương Vân Nga đã trao ngôi vua cho ai?", "options": ["Lê Hoàn", "Đinh Toàn", "Lý Công Uẩn", "Ngô Nhật Khánh"], "answer": "Lê Hoàn"},
            {"q": "Đinh Bộ Lĩnh dẹp loạn 12 sứ quân vào năm nào?", "options": ["967", "968", "966", "969"], "answer": "967"},
            {"q": "Đinh Bộ Lĩnh được tôn xưng là gì?", "options": ["Đinh Tiên Hoàng", "Đinh Thái Tổ", "Đinh Thái Tông", "Đinh Cao Tông"], "answer": "Đinh Tiên Hoàng"},
            {"q": "Nhà Đinh tồn tại bao nhiêu năm?", "options": ["12", "13", "14", "15"], "answer": "12"},
        ],
        "TIỀN LÊ": [
            {"q": "Người sáng lập nhà Tiền Lê là ai?", "options": ["Lê Hoàn", "Lê Long Đĩnh", "Lê Thái Tổ", "Lê Thánh Tông"], "answer": "Lê Hoàn"},
            {"q": "Lê Hoàn lên ngôi năm nào?", "options": ["980", "981", "979", "968"], "answer": "980"},
            {"q": "Lê Hoàn đánh bại quân xâm lược nào?", "options": ["Tống", "Mông - Nguyên", "Minh", "Thanh"], "answer": "Tống"},
            {"q": "Lê Hoàn được biết đến với danh hiệu gì?", "options": ["Lê Đại Hành", "Lê Thái Tổ", "Lê Thánh Tông", "Lê Nhân Tông"], "answer": "Lê Đại Hành"},
            {"q": "Ai là vị vua cuối cùng của nhà Tiền Lê?", "options": ["Lê Long Đĩnh", "Lê Ngọa Triều", "Cả hai đều đúng", "Lê Long Việt"], "answer": "Cả hai đều đúng"},
            {"q": "Lê Long Đĩnh nổi tiếng với thú vui gì?", "options": ["Nằm xem kịch", "Chơi trống", "Đúc tượng", "Làm thơ"], "answer": "Nằm xem kịch"},
            {"q": "Nhà Tiền Lê tồn tại bao nhiêu năm?", "options": ["29", "30", "31", "32"], "answer": "29"},
            {"q": "Kinh đô nhà Tiền Lê đặt ở đâu?", "options": ["Hoa Lư", "Thăng Long", "Cổ Loa", "Tây Đô"], "answer": "Hoa Lư"},
            {"q": "Chiến thắng nào của Lê Hoàn diễn ra trên sông Bạch Đằng?", "options": ["Năm 981", "Năm 938", "Năm 1288", "Năm 1789"], "answer": "Năm 981"},
            {"q": "Ai là vợ của cả Đinh Tiên Hoàng và Lê Đại Hành?", "options": ["Dương Vân Nga", "Ỷ Lan", "Tuyên Từ Thái hậu", "Linh Từ Quốc Mẫu"], "answer": "Dương Vân Nga"},
        ],
        "NHÀ LÝ": [
            {"q": "Người sáng lập nhà Lý là ai?", "options": ["Lý Thánh Tông", "Lý Nhân Tông", "Lý Công Uẩn", "Trần Thái Tông"], "answer": "Lý Công Uẩn"},
            {"q": "Lý Công Uẩn dời đô về Thăng Long năm nào?", "options": ["1009", "1010", "1011", "1012"], "answer": "1010"},
            {"q": "Chiếu dời đô của Lý Công Uẩn có tên là gì?", "options": ["Chiếu Cần Vương", "Chiếu dời đô", "Hịch tướng sĩ", "Bình Ngô đại cáo"], "answer": "Chiếu dời đô"},
            {"q": "Vị vua thứ hai của nhà Lý là ai?", "options": ["Lý Thái Tông", "Lý Thánh Tông", "Lý Nhân Tông", "Lý Anh Tông"], "answer": "Lý Thái Tông"},
            {"q": "Lý Thánh Tông đặt tên nước là gì?", "options": ["Đại Việt", "Đại Cồ Việt", "Đại Nam", "Việt Nam"], "answer": "Đại Việt"},
            {"q": "Văn Miếu - Quốc Tử Giám được xây dựng dưới triều vua nào?", "options": ["Lý Thánh Tông", "Lý Nhân Tông", "Lý Cao Tông", "Lý Anh Tông"], "answer": "Lý Thánh Tông"},
            {"q": "Khoa thi Nho học đầu tiên được tổ chức năm nào?", "options": ["1075", "1070", "1076", "1080"], "answer": "1075"},
            {"q": "Người thầy dạy của Lý Nhân Tông là ai?", "options": ["Lê Văn Thịnh", "Chu Văn An", "Nguyễn Trãi", "Lê Quý Đôn"], "answer": "Lê Văn Thịnh"},
            {"q": "Nhà Lý có bao nhiêu đời vua?", "options": ["8", "9", "10", "11"], "answer": "9"},
            {"q": "Nhà Lý sụp đổ năm nào?", "options": ["1225", "1226", "1227", "1228"], "answer": "1225"},
        ],
        "NHÀ TRẦN": [
            {"q": "Nhà Trần thành lập năm nào?", "options": ["1009", "1225", "1400", "1788"], "answer": "1225"},
            {"q": "Vị vua đầu tiên của nhà Trần là ai?", "options": ["Trần Thái Tông", "Trần Nhân Tông", "Trần Thánh Tông", "Trần Anh Tông"], "answer": "Trần Thái Tông"},
            {"q": "Nhà Trần đã bao lần đánh thắng quân Mông - Nguyên?", "options": ["1", "2", "3", "4"], "answer": "3"},
            {"q": "Hội nghị Diên Hồng diễn ra vào năm nào?", "options": ["1284", "1285", "1288", "1258"], "answer": "1284"},
            {"q": "Trần Hưng Đạo có tên thật là gì?", "options": ["Trần Quốc Tuấn", "Trần Quang Khải", "Trần Nhật Duật", "Trần Khánh Dư"], "answer": "Trần Quốc Tuấn"},
            {"q": "Câu nói 'Đầu thần chưa rơi xuống đất, xin bệ hạ đừng lo' là của ai?", "options": ["Trần Thủ Độ", "Trần Quốc Tuấn", "Trần Quang Khải", "Lê Phụ Trần"], "answer": "Trần Thủ Độ"},
            {"q": "Chiến thắng Bạch Đằng năm 1288 do ai chỉ huy?", "options": ["Trần Hưng Đạo", "Trần Quang Khải", "Trần Nhật Duật", "Trần Bình Trọng"], "answer": "Trần Hưng Đạo"},
            {"q": "Câu nói 'Ta thà làm quỷ nước Nam chứ không thèm làm vương đất Bắc' là của ai?", "options": ["Trần Bình Trọng", "Trần Quốc Toản", "Phạm Ngũ Lão", "Yết Kiêu"], "answer": "Trần Bình Trọng"},
            {"q": "Nhà Trần truyền ngôi theo lệ gì?", "options": ["Thái thượng hoàng", "Cha truyền con nối", "Anh truyền em", "Bầu chọn"], "answer": "Thái thượng hoàng"},
            {"q": "Hịch tướng sĩ là tác phẩm của ai?", "options": ["Trần Hưng Đạo", "Nguyễn Trãi", "Lý Thường Kiệt", "Trần Quang Khải"], "answer": "Trần Hưng Đạo"},
        ],
        "NHÀ HỒ": [
            {"q": "Người sáng lập nhà Hồ là ai?", "options": ["Hồ Quý Ly", "Hồ Hán Thương", "Hồ Nguyên Trừng", "Hồ Tông Thốc"], "answer": "Hồ Quý Ly"},
            {"q": "Hồ Quý Ly lên ngôi năm nào?", "options": ["1400", "1399", "1401", "1398"], "answer": "1400"},
            {"q": "Nhà Hồ đặt quốc hiệu là gì?", "options": ["Đại Ngu", "Đại Việt", "Đại Cồ Việt", "Đại Nam"], "answer": "Đại Ngu"},
            {"q": "Kinh đô nhà Hồ đặt ở đâu?", "options": ["Tây Đô (Thanh Hóa)", "Đông Đô (Hà Nội)", "Phú Xuân", "Hoa Lư"], "answer": "Tây Đô (Thanh Hóa)"},
            {"q": "Hồ Quý Ly thực hiện cải cách gì nổi tiếng?", "options": ["Hạn điền, hạn nô", "Quân điền", "Bình quân ruộng đất", "Chế độ lộc điền"], "answer": "Hạn điền, hạn nô"},
            {"q": "Hồ Quý Ly phát hành loại tiền giấy đầu tiên gọi là gì?", "options": ["Thông bảo hội sao", "Tiền đồng", "Tiền kẽm", "Bảo sao"], "answer": "Thông bảo hội sao"},
            {"q": "Nhà Hồ bị quân Minh xâm lược vào năm nào?", "options": ["1406", "1407", "1408", "1405"], "answer": "1406"},
            {"q": "Thành nhà Hồ thuộc tỉnh nào ngày nay?", "options": ["Thanh Hóa", "Nghệ An", "Hà Tĩnh", "Quảng Bình"], "answer": "Thanh Hóa"},
            {"q": "Hồ Quý Ly và Hồ Hán Thương bị bắt trong trận nào?", "options": ["Trận Hàm Tử", "Trận Chi Lăng", "Trận Đa Bang", "Trận Tốt Động"], "answer": "Trận Đa Bang"},
            {"q": "Nhà Hồ tồn tại bao nhiêu năm?", "options": ["7", "8", "9", "10"], "answer": "7"},
        ],
        "LAM SƠN - LÊ SƠ": [
            {"q": "Lê Lợi dựng cờ khởi nghĩa Lam Sơn năm nào?", "options": ["1418", "1427", "1428", "1416"], "answer": "1418"},
            {"q": "Hội thề Lũng Nhai có sự tham gia của bao nhiêu người?", "options": ["18", "19", "20", "21"], "answer": "18"},
            {"q": "Nguyễn Trãi dâng Bình Ngô sách cho Lê Lợi ở đâu?", "options": ["Nghệ An", "Thanh Hóa", "Lạng Sơn", "Hà Nội"], "answer": "Nghệ An"},
            {"q": "Trận Chi Lăng - Xương Giang quyết định thắng lợi khởi nghĩa Lam Sơn diễn ra năm nào?", "options": ["1427", "1428", "1426", "1425"], "answer": "1427"},
            {"q": "Lê Lợi lên ngôi Hoàng đế năm nào?", "options": ["1428", "1427", "1429", "1430"], "answer": "1428"},
            {"q": "Bình Ngô đại cáo do ai viết?", "options": ["Nguyễn Trãi", "Lê Lợi", "Lê Thánh Tông", "Ngô Sĩ Liên"], "answer": "Nguyễn Trãi"},
            {"q": "Vị vua nào của nhà Lê sơ ban hành bộ luật Hồng Đức?", "options": ["Lê Thánh Tông", "Lê Thái Tổ", "Lê Nhân Tông", "Lê Hiến Tông"], "answer": "Lê Thánh Tông"},
            {"q": "Lê Thánh Tông lập Hội Tao Đàn gồm bao nhiêu vị?", "options": ["28", "27", "29", "30"], "answer": "28"},
            {"q": "Vụ án Lệ Chi Viên liên quan đến cái chết của ai?", "options": ["Nguyễn Trãi", "Lê Lai", "Trần Nguyên Hãn", "Phạm Văn Xảo"], "answer": "Nguyễn Trãi"},
            {"q": "Nhà Lê sơ kết thúc khi nào?", "options": ["1527", "1526", "1528", "1529"], "answer": "1527"},
        ],
        "NHÀ MẠC": [
            {"q": "Người sáng lập nhà Mạc là ai?", "options": ["Mạc Đăng Dung", "Mạc Đăng Doanh", "Mạc Kính Cung", "Mạc Mậu Hợp"], "answer": "Mạc Đăng Dung"},
            {"q": "Mạc Đăng Dung cướp ngôi nhà Lê sơ năm nào?", "options": ["1527", "1528", "1529", "1530"], "answer": "1527"},
            {"q": "Nhà Mạc đóng đô ở đâu?", "options": ["Thăng Long", "Tây Đô", "Cao Bằng", "Hoa Lư"], "answer": "Thăng Long"},
            {"q": "Chiến tranh Nam - Bắc triều diễn ra giữa hai thế lực nào?", "options": ["Lê Trung Hưng và Mạc", "Trịnh và Nguyễn", "Tây Sơn và Nguyễn Ánh", "Đàng Ngoài và Đàng Trong"], "answer": "Lê Trung Hưng và Mạc"},
            {"q": "Nhà Mạc thất bại, phải rút lên vùng nào?", "options": ["Cao Bằng", "Lạng Sơn", "Thái Nguyên", "Tuyên Quang"], "answer": "Cao Bằng"},
            {"q": "Mạc Đăng Dung trước khi làm vua từng giữ chức gì dưới triều Lê?", "options": ["Thái sư", "Thái úy", "Tể tướng", "Đại tư đồ"], "answer": "Thái sư"},
            {"q": "Nhà Mạc tồn tại ở Cao Bằng đến năm nào?", "options": ["1677", "1675", "1680", "1666"], "answer": "1677"},
            {"q": "Nhà Mạc đã tổ chức bao nhiêu kỳ thi Hội?", "options": ["22", "21", "23", "24"], "answer": "22"},
            {"q": "Thời Mạc, thương mại phát triển mạnh ở đô thị nào?", "options": ["Thăng Long", "Phố Hiến", "Hội An", "Vân Đồn"], "answer": "Thăng Long"},
            {"q": "Vị vua cuối cùng của nhà Mạc là ai?", "options": ["Mạc Kính Vũ", "Mạc Mậu Hợp", "Mạc Kính Cung", "Mạc Toàn"], "answer": "Mạc Kính Vũ"},
        ],
        "TRỊNH - NGUYỄN PHÂN TRANH": [
            {"q": "Cuộc chiến Trịnh - Nguyễn phân tranh kéo dài bao nhiêu năm?", "options": ["Gần 50 năm", "Gần 100 năm", "Gần 150 năm", "Gần 200 năm"], "answer": "Gần 50 năm"},
            {"q": "Sông Gianh là ranh giới phân chia Đàng Trong và Đàng Ngoài vào thời nào?", "options": ["Trịnh - Nguyễn", "Lê - Mạc", "Tây Sơn - Nguyễn Ánh", "Lý - Trần"], "answer": "Trịnh - Nguyễn"},
            {"q": "Chúa Nguyễn đầu tiên ở Đàng Trong là ai?", "options": ["Nguyễn Hoàng", "Nguyễn Kim", "Nguyễn Phúc Nguyên", "Nguyễn Phúc Tần"], "answer": "Nguyễn Hoàng"},
            {"q": "Chúa Trịnh đầu tiên ở Đàng Ngoài là ai?", "options": ["Trịnh Kiểm", "Trịnh Tùng", "Trịnh Tráng", "Trịnh Tạc"], "answer": "Trịnh Kiểm"},
            {"q": "Chúa Nguyễn Hoàng vào trấn thủ Thuận Hóa năm nào?", "options": ["1558", "1545", "1570", "1600"], "answer": "1558"},
            {"q": "Cuộc chiến Trịnh - Nguyễn kết thúc bằng sự kiện gì?", "options": ["Khởi nghĩa Tây Sơn lật đổ cả hai tập đoàn", "Nguyễn Ánh thống nhất đất nước", "Quân Trịnh chiếm được Phú Xuân", "Hiệp ước chấm dứt chiến tranh"], "answer": "Khởi nghĩa Tây Sơn lật đổ cả hai tập đoàn"},
            {"q": "Lũy Thầy (ở Quảng Bình) do ai xây dựng?", "options": ["Đào Duy Từ", "Nguyễn Hữu Cảnh", "Trịnh Kiểm", "Nguyễn Hoàng"], "answer": "Đào Duy Từ"},
            {"q": "Thời Trịnh - Nguyễn, Đàng Trong còn được gọi là gì?", "options": ["Xứ Đàng Trong", "Nam Hà", "Giao Chỉ", "An Nam"], "answer": "Xứ Đàng Trong"},
            {"q": "Phố Hiến là trung tâm thương mại sầm uất của Đàng Ngoài, còn Hội An là của Đàng Trong.", "options": ["Đúng", "Sai", "Không xác định", "Cả hai đều ở Đàng Ngoài"], "answer": "Đúng"},
            {"q": "Ai là người có công mở rộng lãnh thổ Đàng Trong xuống phía Nam?", "options": ["Nguyễn Hữu Cảnh", "Nguyễn Hoàng", "Nguyễn Phúc Chu", "Nguyễn Ánh"], "answer": "Nguyễn Hữu Cảnh"},
        ],
        "TÂY SƠN": [
            {"q": "Khởi nghĩa Tây Sơn do ai lãnh đạo?", "options": ["Nguyễn Nhạc, Nguyễn Huệ, Nguyễn Lữ", "Nguyễn Huệ, Nguyễn Ánh", "Trịnh Kiểm, Nguyễn Kim", "Lê Lợi, Nguyễn Trãi"], "answer": "Nguyễn Nhạc, Nguyễn Huệ, Nguyễn Lữ"},
            {"q": "Nguyễn Huệ lên ngôi Hoàng đế lấy hiệu là gì?", "options": ["Quang Trung", "Thái Đức", "Cảnh Thịnh", "Gia Long"], "answer": "Quang Trung"},
            {"q": "Chiến thắng Ngọc Hồi - Đống Đa diễn ra vào năm nào?", "options": ["1789", "1788", "1787", "1790"], "answer": "1789"},
            {"q": "Quang Trung đại phá quân Thanh vào dịp Tết năm nào?", "options": ["Kỷ Dậu 1789", "Mậu Thân 1788", "Bính Ngọ 1786", "Đinh Mùi 1787"], "answer": "Kỷ Dậu 1789"},
            {"q": "Trước khi đánh quân Thanh, Nguyễn Huệ làm lễ lên ngôi ở đâu?", "options": ["Phú Xuân", "Thăng Long", "Quy Nhơn", "Thanh Hóa"], "answer": "Phú Xuân"},
            {"q": "Chiếu khuyến nông, Chiếu lập học là chính sách của vị vua nào?", "options": ["Quang Trung", "Gia Long", "Minh Mạng", "Lê Thánh Tông"], "answer": "Quang Trung"},
            {"q": "Nguyễn Huệ đánh tan quân Xiêm trong trận nào?", "options": ["Rạch Gầm - Xoài Mút", "Ngọc Hồi - Đống Đa", "Bạch Đằng", "Chi Lăng"], "answer": "Rạch Gầm - Xoài Mút"},
            {"q": "Nhà Tây Sơn sụp đổ năm nào?", "options": ["1802", "1801", "1803", "1804"], "answer": "1802"},
            {"q": "Quang Trung mất năm nào?", "options": ["1792", "1793", "1794", "1795"], "answer": "1792"},
            {"q": "Vị vua cuối cùng của nhà Tây Sơn là ai?", "options": ["Nguyễn Quang Toản", "Nguyễn Nhạc", "Nguyễn Lữ", "Nguyễn Văn Bảo"], "answer": "Nguyễn Quang Toản"},
        ],
        "NHÀ NGUYỄN": [
            {"q": "Nguyễn Ánh lên ngôi Hoàng đế năm nào?", "options": ["1802", "1803", "1804", "1805"], "answer": "1802"},
            {"q": "Niên hiệu của Nguyễn Ánh là gì?", "options": ["Gia Long", "Minh Mạng", "Thiệu Trị", "Tự Đức"], "answer": "Gia Long"},
            {"q": "Kinh đô nhà Nguyễn đặt ở đâu?", "options": ["Phú Xuân (Huế)", "Thăng Long", "Hoa Lư", "Sài Gòn"], "answer": "Phú Xuân (Huế)"},
            {"q": "Nhà Nguyễn đã ban hành bộ luật nào?", "options": ["Hoàng Việt luật lệ", "Hồng Đức", "Quốc triều hình luật", "Hình thư"], "answer": "Hoàng Việt luật lệ"},
            {"q": "Vua Tự Đức trị vì bao nhiêu năm?", "options": ["36", "35", "37", "38"], "answer": "36"},
            {"q": "Phong trào Cần Vương diễn ra dưới thời vua nào?", "options": ["Hàm Nghi", "Tự Đức", "Dục Đức", "Hiệp Hòa"], "answer": "Hàm Nghi"},
            {"q": "Nhà Nguyễn ký Hiệp ước nào nhường ba tỉnh miền Đông Nam Kỳ cho Pháp?", "options": ["Nhâm Tuất 1862", "Giáp Tuất 1874", "Hác Măng 1883", "Patơnốt 1884"], "answer": "Nhâm Tuất 1862"},
            {"q": "Vị vua nào của nhà Nguyễn có tinh thần chống Pháp mạnh mẽ, từng nói 'Đánh hay là hòa, quyền ở nơi ta'?", "options": ["Tự Đức", "Minh Mạng", "Thiệu Trị", "Hàm Nghi"], "answer": "Tự Đức"},
            {"q": "Nhà Nguyễn có bao nhiêu đời vua?", "options": ["13", "12", "14", "15"], "answer": "13"},
            {"q": "Vua Bảo Đại thoái vị năm nào?", "options": ["1945", "1946", "1947", "1948"], "answer": "1945"},
        ],
        "CHỐNG PHÁP": [
            {"q": "Thực dân Pháp nổ súng xâm lược Việt Nam lần đầu tiên ở đâu?", "options": ["Đà Nẵng", "Sài Gòn", "Hà Nội", "Hải Phòng"], "answer": "Đà Nẵng"},
            {"q": "Ai là người lãnh đạo phong trào Cần Vương?", "options": ["Vua Hàm Nghi và Tôn Thất Thuyết", "Phan Đình Phùng", "Hoàng Hoa Thám", "Nguyễn Trường Tộ"], "answer": "Vua Hàm Nghi và Tôn Thất Thuyết"},
            {"q": "Khởi nghĩa Yên Thế do ai lãnh đạo?", "options": ["Hoàng Hoa Thám", "Phan Đình Phùng", "Nguyễn Thiện Thuật", "Tôn Thất Thuyết"], "answer": "Hoàng Hoa Thám"},
            {"q": "Nguyễn Tất Thành ra đi tìm đường cứu nước vào năm nào?", "options": ["1911", "1912", "1913", "1914"], "answer": "1911"},
            {"q": "Phong trào Đông Du do ai khởi xướng?", "options": ["Phan Bội Châu", "Phan Châu Trinh", "Lương Văn Can", "Nguyễn Quyền"], "answer": "Phan Bội Châu"},
            {"q": "Cuộc khai thác thuộc địa lần thứ nhất của Pháp ở Việt Nam bắt đầu năm nào?", "options": ["1897", "1896", "1898", "1899"], "answer": "1897"},
            {"q": "Ai là người sáng lập Đông Kinh nghĩa thục?", "options": ["Lương Văn Can, Nguyễn Quyền", "Phan Bội Châu", "Phan Châu Trinh", "Huỳnh Thúc Kháng"], "answer": "Lương Văn Can, Nguyễn Quyền"},
            {"q": "Phong trào Duy Tân ở Trung Kỳ do ai lãnh đạo?", "options": ["Phan Châu Trinh", "Phan Bội Châu", "Trần Cao Vân", "Thái Phiên"], "answer": "Phan Châu Trinh"},
            {"q": "Cuộc bãi công của công nhân Ba Son diễn ra năm nào?", "options": ["1925", "1924", "1926", "1927"], "answer": "1925"},
            {"q": "Hội Việt Nam Cách mạng Thanh niên do ai sáng lập?", "options": ["Nguyễn Ái Quốc", "Trần Phú", "Lê Hồng Phong", "Hà Huy Tập"], "answer": "Nguyễn Ái Quốc"},
        ],
        "CHỐNG MỸ": [
            {"q": "Hiệp định Genève chia đôi đất nước ta tại vĩ tuyến bao nhiêu?", "options": ["17", "16", "18", "19"], "answer": "17"},
            {"q": "Phong trào Đồng Khởi nổ ra đầu tiên ở đâu?", "options": ["Bến Tre", "Mỹ Tho", "Trà Vinh", "Vĩnh Long"], "answer": "Bến Tre"},
            {"q": "Chiến thắng Ấp Bắc diễn ra năm nào?", "options": ["1963", "1962", "1964", "1965"], "answer": "1963"},
            {"q": "Sự kiện Vịnh Bắc Bộ xảy ra năm nào?", "options": ["1964", "1963", "1965", "1966"], "answer": "1964"},
            {"q": "Chiến dịch nào mở màn cho cuộc Tổng tiến công và nổi dậy Xuân Mậu Thân 1968?", "options": ["Đường 9 - Khe Sanh", "Tây Nguyên", "Huế - Đà Nẵng", "Sài Gòn"], "answer": "Đường 9 - Khe Sanh"},
            {"q": "Chiến dịch Điện Biên Phủ trên không diễn ra vào tháng mấy, năm nào?", "options": ["Tháng 12/1972", "Tháng 12/1971", "Tháng 5/1972", "Tháng 4/1975"], "answer": "Tháng 12/1972"},
            {"q": "Hiệp định Paris về chấm dứt chiến tranh ở Việt Nam được ký kết năm nào?", "options": ["1973", "1972", "1974", "1975"], "answer": "1973"},
            {"q": "Chiến dịch Hồ Chí Minh kết thúc thắng lợi vào ngày tháng năm nào?", "options": ["30/4/1975", "1/5/1975", "2/5/1975", "29/4/1975"], "answer": "30/4/1975"},
            {"q": "Ai là Tổng tư lệnh chiến dịch Hồ Chí Minh?", "options": ["Đại tướng Văn Tiến Dũng", "Đại tướng Võ Nguyên Giáp", "Đại tướng Hoàng Văn Thái", "Thượng tướng Trần Văn Trà"], "answer": "Đại tướng Văn Tiến Dũng"},
            {"q": "Xe tăng húc đổ cổng Dinh Độc Lập mang số hiệu bao nhiêu?", "options": ["390 và 843", "390 và 845", "843 và 390", "845 và 390"], "answer": "390 và 843"},
        ],
        "BIÊN GIỚI - BẢO VỆ TỔ QUỐC": [
            {"q": "Chiến dịch Biên giới thu đông 1950 diễn ra dưới sự chỉ huy trực tiếp của ai?", "options": ["Võ Nguyên Giáp", "Hoàng Văn Thái", "Trường Chinh", "Phạm Văn Đồng"], "answer": "Võ Nguyên Giáp"},
            {"q": "Chiến tranh biên giới Tây Nam kết thúc năm nào?", "options": ["1979", "1978", "1980", "1981"], "answer": "1979"},
            {"q": "Chiến dịch phản công biên giới phía Bắc diễn ra vào tháng mấy, năm 1979?", "options": ["Tháng 2", "Tháng 3", "Tháng 4", "Tháng 5"], "answer": "Tháng 2"},
            {"q": "Luật Biên giới quốc gia được Quốc hội thông qua năm nào?", "options": ["2003", "2001", "2005", "2012"], "answer": "2003"},
            {"q": "Việt Nam và Trung Quốc ký Hiệp ước biên giới trên đất liền năm nào?", "options": ["1999", "2000", "1998", "2001"], "answer": "1999"},
            {"q": "Ngày Biên phòng toàn dân là ngày nào?", "options": ["3/3", "22/12", "30/4", "19/8"], "answer": "3/3"},
            {"q": "Ai là vị tướng đầu tiên của Quân đội Nhân dân Việt Nam?", "options": ["Võ Nguyên Giáp", "Nguyễn Chí Thanh", "Hoàng Văn Thái", "Văn Tiến Dũng"], "answer": "Võ Nguyên Giáp"},
            {"q": "Chiến dịch nào đánh dấu bước phát triển mới của bộ đội chủ lực ta trong kháng chiến chống Pháp?", "options": ["Biên giới 1950", "Việt Bắc 1947", "Điện Biên Phủ 1954", "Tây Bắc 1952"], "answer": "Biên giới 1950"},
            {"q": "Mốc biên giới số 0 nằm ở tỉnh nào?", "options": ["Điện Biên", "Lai Châu", "Lào Cai", "Hà Giang"], "answer": "Điện Biên"},
            {"q": "Lực lượng nào là nòng cốt trong bảo vệ chủ quyền biên giới quốc gia?", "options": ["Bộ đội Biên phòng", "Công an nhân dân", "Dân quân tự vệ", "Cảnh sát biển"], "answer": "Bộ đội Biên phòng"},
        ],
    }
    return render(request, 'question.html', {'data': data})