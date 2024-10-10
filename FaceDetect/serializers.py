from django import forms
from FaceDetect.models import EyeModel

class EyeImageForm(forms.ModelForm):
    class Meta:
        model = EyeModel
        fields = ['eye_name', 'eye_image']
