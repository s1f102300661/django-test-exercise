from django.db import models
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    GENRE_CHOICES = [
        ('report', 'Report'),
        ('program', 'Program'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    posted_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField(null=True, blank=True)
    favorite = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='other')
    
    def is_overdue(self, dt):
        if self.due_at is None:
            return False
        return self.due_at < dt
