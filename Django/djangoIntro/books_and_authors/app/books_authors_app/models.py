from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # related_name = 'authors'

class Author(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    books = models.ManyToManyField(Book, related_name='authors')