from django.db import models
from Accounts.models import User
# Create your models here.
import uuid
podcast_data_file_type= (
    ("Audio","AUDIO"),
    ("Video","VIDEO"),
)
class podcast_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postid = models.UUIDField(default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=100)
    thumbnail = models.FileField(upload_to='thumbnail')
    description = models.TextField()
    type = models.CharField(max_length=100,default="",blank=True,choices=podcast_data_file_type)
    likes = models.IntegerField(default=0)
    speaker = models.CharField(max_length=255)
    file = models.FileField(upload_to='podcast')
    
    def __str__(self):
        return self.title

class Favorite_podcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    podcast = models.ForeignKey(podcast_data, on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    class Meta:
        unique_together = ('user', 'podcast',)    