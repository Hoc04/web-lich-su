from django.test import TestCase
from .models import Dynasty, Book

class HistoryWebTest(TestCase):
    
    def setUp(self):
        # Thiết lập dữ liệu giả lập để test
        self.dynasty = Dynasty.objects.create(name="NHÀ TRẦN")
        self.book = Book.objects.create(
            title="Sử Việt - 12 Khúc Tráng Ca", 
            price=150000,
            image_url="http://example.com/image.jpg"
        )

    # 1. Kiểm tra Model xem có lưu đúng không
    def test_model_creation(self):
        self.assertEqual(self.dynasty.name, "NHÀ TRẦN")
        self.assertEqual(self.book.price, 150000)

    # 2. Kiểm tra trang chủ có hoạt động không (Status 200)
    def test_book_store_view(self):
     response = self.client.get('/cua-hang/')
     print("Status:", response.status_code)
     print("URL called:", response.request['PATH_INFO'])
     self.assertEqual(response.status_code, 200)

    # 3. Kiểm tra trang cửa hàng sách có hiển thị đúng không
    def test_book_store_view(self):
        response = self.client.get('/store/') # Thay bằng URL của bạn
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "12 Khúc Tráng Ca")
    
