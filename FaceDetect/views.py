from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EyeModel
from .serializers import EyeImageForm

class UploadEyeImagesAPIView(APIView):

    def get(self, request, format=None):
        eye_images = EyeModel.objects.all()
        serializer = EyeImageForm(eye_images, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = EyeImageForm(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
