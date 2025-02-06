from core.models import BaseModel
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Notification(BaseModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_read"]),  # Faster queries for unread notifications
        ]
        
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read"])
            
    def __str__(self):
        return f"Notification({self.title}) for {self.user}"