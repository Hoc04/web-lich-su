from django.contrib import admin
from .models import Dynasty, Question, Book, Order

@admin.register(Dynasty)
class DynastyAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'dynasty', 'correct_answer')
    list_filter = ('dynasty',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'book', 'status', 'created_at')
    list_filter = ('status',)