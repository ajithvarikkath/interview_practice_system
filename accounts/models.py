from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner (0-2 years)'),
        ('Intermediate', 'Intermediate (2-5 years)'),
        ('Advanced', 'Advanced (5+ years)'),
    ]
    
    FOCUS_CHOICES = [
        ('Software Engineering', 'Software Engineering'),
        ('Data Science', 'Data Science & ML'),
        ('Product Management', 'Product Management'),
        ('System Design', 'System Design & Architecture'),
    ]

    bio = models.TextField(blank=True, null=True, help_text="Brief description about your background.")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="Upload a profile picture.")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Beginner')
    focus_area = models.CharField(max_length=50, choices=FOCUS_CHOICES, default='Software Engineering')
    
    def __str__(self):
        return self.username
