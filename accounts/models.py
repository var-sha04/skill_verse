from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    college_id = models.CharField(max_length=50, unique=True)
    student_id = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    # Common fields
    department = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    # Student-specific
    previous_education = models.CharField(max_length=200, blank=True, null=True)
    current_education = models.CharField(max_length=200, blank=True, null=True)

    # Faculty-specific
    subjects_taught = models.CharField(max_length=255, blank=True, null=True,
                                       help_text="Comma-separated subjects")
    experience = models.TextField(blank=True, null=True)

    # Skills (common)
    skills = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"





class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:20]}"

class FacultyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='faculty_photos/', blank=True, null=True)
    department = models.CharField(max_length=100)
    subjects_taught = models.CharField(max_length=255, help_text="Comma-separated subjects")

    def __str__(self):
        return self.user.get_full_name() or self.user.username
# Create your models here.
