from django.urls import path
from .views import UploadEyeImagesAPIView

urlpatterns = [
    path('api/eye-images/', UploadEyeImagesAPIView.as_view(), name='upload_eye_images'),
]