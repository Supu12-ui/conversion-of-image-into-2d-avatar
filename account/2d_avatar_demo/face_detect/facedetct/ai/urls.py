from django.urls import path
from .views import upload_avatar
from django.conf import settings
from django.conf.urls.static import static

from ai import views
# from views import EyeOverlayView
urlpatterns = [
    path('upload/', views.upload_avatar, name='upload_image'),
    # path('eye/', EyeOverlayView.as_view(), name='upload_image'),

] 