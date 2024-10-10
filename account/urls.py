from django.urls import path,include
from account.views import  UploadEyeImagesView, UserRegistrationViews, UserLoginView, UserProfileView, UserChangePasswordView, AvatarImageView, GenderUserView, SunglassView

urlpatterns = [
    path('register/', UserRegistrationViews.as_view(), name = 'register'),
    path('login/', UserLoginView.as_view(), name = 'login'),
    path('userprofile/', UserProfileView.as_view(), name = 'userprofile'),
    path('changepassword/', UserChangePasswordView.as_view(), name = 'userpassword'),
    path('gender/', GenderUserView.as_view(), name='profile-update'),
    path('avatar/', AvatarImageView.as_view(), name = 'Avatar Image'),
    path('sunglass/', SunglassView.as_view(), name='upload_eye_images'),  

]