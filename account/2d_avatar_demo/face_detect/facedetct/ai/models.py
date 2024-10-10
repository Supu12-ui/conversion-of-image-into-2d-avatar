# models.py

from django.db import models

class Avatar(models.Model):
    avatar_url = models.URLField()  
    sunglasses_image = models.URLField()

    def __str__(self):
        return self.avatar_url
    
class Eye(models.Model):
    avatar_url = models.URLField()
    left_eye = models.ImageField(upload_to= 'left-eye/')
    right_eye = models.ImageField(upload_to= 'right-eye/')

