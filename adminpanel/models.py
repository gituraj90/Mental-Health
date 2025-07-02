from django.db import models
import uuid

from django.contrib.auth import get_user_model
User = get_user_model()

class ChatRecord(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.UUIDField(null=True, blank=True)
    guest_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp} - {self.guest_name or (self.user.username if self.user else 'Unknown')}"
    

    

class GalleryItem(models.Model):
    title = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)  # ✅ new caption field
    image = models.ImageField(upload_to='gallery/')
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class CKEditorContent(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Content', config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    
