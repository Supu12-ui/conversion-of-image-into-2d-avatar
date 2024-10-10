from django.db import models

class EyeModel(models.Model):
    eye_id = models.AutoField(primary_key=True)
    eye_name = models.CharField(max_length=255)
    eye_image = models.ImageField(upload_to='eye_image/')

