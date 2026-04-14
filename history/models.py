from django.db import models
class Event(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

class Video(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()

class Question(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
