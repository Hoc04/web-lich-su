from django.db import models

# Quản lý Triều đại
class Dynasty(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên triều đại")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")

    def __str__(self):
        return self.name

# Quản lý Câu hỏi (Liên kết với Triều đại)
class Question(models.Model):
    dynasty = models.ForeignKey(Dynasty, on_delete=models.CASCADE, related_name='questions', verbose_name="Triều đại")
    text = models.TextField(verbose_name="Nội dung câu hỏi")
    option_a = models.CharField(max_length=200, verbose_name="Đáp án A")
    option_b = models.CharField(max_length=200, verbose_name="Đáp án B")
    option_c = models.CharField(max_length=200, verbose_name="Đáp án C")
    option_d = models.CharField(max_length=200, verbose_name="Đáp án D")
    correct_answer = models.CharField(max_length=200, verbose_name="Đáp án đúng")

    def __str__(self):
        return self.text

# Quản lý Sách
class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tên sách")
    image_url = models.URLField(verbose_name="URL ảnh bìa")  # Dùng link ảnh bạn cung cấp
    price = models.IntegerField(default=0, verbose_name="Giá (VNĐ)")
    description = models.TextField(verbose_name="Mô tả")

    def __str__(self):
        return self.title

# Quản lý Đơn hàng
class Order(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Sách")
    order_code = models.CharField(max_length=50, unique=True, verbose_name="Mã đơn hàng")
    customer_email = models.EmailField(verbose_name="Email khách hàng")
    status = models.BooleanField(default=False, verbose_name="Trạng thái thanh toán")  # False: Chờ, True: Đã thanh toán
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")

    def __str__(self):
        return f"Đơn hàng {self.order_code} - {self.customer_email}"