from django.db import models

class Dynasty(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên triều đại")
    
    def __str__(self):
        return self.name

class Question(models.Model):
    dynasty = models.ForeignKey(Dynasty, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name="Nội dung câu hỏi")
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200, verbose_name="Đáp án đúng")

    def __str__(self):
        return self.text