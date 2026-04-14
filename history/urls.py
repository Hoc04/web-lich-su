from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/', views.video_page, name='video_page'),
    path('question/', views.question_page, name='question_page'),
]