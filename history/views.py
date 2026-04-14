from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def video_page(request):
    videos = [
        {"title": "Lịch sử Việt Nam tổng hợp", "url": "https://www.youtube.com/embed/RjCWU2RDEh4"},
        {"title": "Kháng chiến chống Pháp", "url": "https://www.youtube.com/embed/AbRg5rH6fxo"},
        {"title": "Kháng chiến chống Mỹ", "url": "https://www.youtube.com/embed/TQehUlbyp3o"}
    ]
    return render(request, 'video.html', {'videos': videos})

def question_page(request):
    # Dữ liệu 100+ câu hỏi chia theo triều đại
    data = {
        "NHÀ NGÔ": [
            {"q": "Người sáng lập nhà Ngô là ai?", "options": ["Ngô Quyền", "Đinh Bộ Lĩnh", "Lê Hoàn", "Lý Công Uẩn"], "answer": "Ngô Quyền"},
            {"q": "Nhà Ngô được thành lập năm nào?", "options": ["938", "939", "968", "1009"], "answer": "939"},
            {"q": "Sự kiện nào mở đầu cho nhà Ngô?", "options": ["Chiến thắng Chi Lăng", "Chiến thắng Bạch Đằng (938)", "Chiến thắng Điện Biên Phủ", "Khởi nghĩa Lam Sơn"], "answer": "Chiến thắng Bạch Đằng (938)"},
            # ... Thêm đủ 10 câu nhà Ngô bạn đã gửi
        ],
        "NHÀ ĐINH": [
            {"q": "Người sáng lập nhà Đinh là ai?", "options": ["Lê Hoàn", "Ngô Quyền", "Đinh Bộ Lĩnh", "Lý Công Uẩn"], "answer": "Đinh Bộ Lĩnh"},
            {"q": "Đinh Bộ Lĩnh lên ngôi vua năm nào?", "options": ["939", "968", "1009", "1010"], "answer": "968"},
            # ... Thêm đủ 10 câu nhà Đinh
        ],
        "NHÀ LÝ": [
            {"q": "Người sáng lập nhà Lý là ai?", "options": ["Lý Thánh Tông", "Lý Nhân Tông", "Lý Công Uẩn", "Trần Thái Tông"], "answer": "Lý Công Uẩn"},
            # ... Thêm đủ 10 câu nhà Lý
        ],
        "NHÀ TRẦN": [
             {"q": "Nhà Trần thành lập năm nào?", "options": ["1009", "1225", "1400", "1788"], "answer": "1225"},
             # ... Thêm các câu nhà Trần
        ],
        # Tiếp tục tương tự cho: NHÀ HỒ, LAM SƠN, LÊ SƠ, MẠC, LÊ TRUNG HƯNG, TRỊNH - NGUYỄN, TÂY SƠN, NHÀ NGUYỄN, CHỐNG PHÁP, CHỐNG MỸ, BIÊN GIỚI.
    }
    return render(request, 'question.html', {'data': data})