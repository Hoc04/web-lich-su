from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/', views.video_page, name='video_page'),
    path('question/', views.question_page, name='question_page'),
    path('cua-hang/', views.book_store, name='book_list'), # Đường dẫn là 'cua-hang/'
]