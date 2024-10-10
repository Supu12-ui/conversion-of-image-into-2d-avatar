import base64
from django.http import JsonResponse
from django.shortcuts import render
from omegaconf import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from account.serializers import EyeImageSerailzer, UserRegistrationSerailzer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer, AvatarImageSerailizer,GenderUserSerailizer,EyeImageSerailzer, SunglassImageSerailzer
from django.contrib.auth import authenticate
from account.renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
import os
import requests
from django.conf import settings
from account.models import Avatar
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import requests
from io import BytesIO
import dlib


mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('/Users/supriya/Downloads/shape_predictor_68_face_landmarks.dat')





def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def overlay_image_alpha(img, overlay, x, y, overlay_size):
    overlay = cv2.resize(overlay, overlay_size)

    b, g, r, a = cv2.split(overlay)
    overlay_rgb = cv2.merge((b, g, r))

    mask = a / 255.0
    for c in range(0, 3):
        img[y:y + overlay.shape[0], x:x + overlay.shape[1], c] = \
            img[y:y + overlay.shape[0], x:x + overlay.shape[1], c] * (1.0 - mask) + overlay_rgb[:, :, c] * mask


class UserRegistrationViews(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format = None):
        serializer = UserRegistrationSerailzer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save();
            token = get_tokens_for_user(user)
            print(user)
            return Response({'token': token,"message":"Registration Successfully"}, status=status.HTTP_201_CREATED)
        #print(serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self, request, format = None):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password');
            user_name = serializer.data.get('name');
            user = authenticate(email= email,password=password)
            
            if user is not None:
                token = get_tokens_for_user(user)
                user_name = getattr(user, 'name', '')
                return Response({"data":{'token': token,'name': user_name,"message":"Login sucessfull"}}, status = status.HTTP_200_OK)
            else:
                return Response({"errors":{'non_field_errors':['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request, format = None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
        # serializer.save();
            return Response({'message':'Password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SendPasswordResestEmail(APIView):
    renderer_classes=[UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password reset link send to your email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GenderUserView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self, request, format = None):
        user = request.user
        serializer = GenderUserSerailizer(user, data=request.data, partial=True)  # Allow partial update

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'data':{'message':'Gender choosen successfully'}}, status=status.HTTP_200_OK)
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AvatarImageView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format = None):
        user = request.user
        image_File= request.FILES.get('image')
        if not image_File:
            return Response({'error':{'message':'Image is not found'}}, status = status.HTTP_400_BAD_REQUEST)
        serializer = AvatarImageSerailizer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            image_instance = Avatar.objects.create(user = user, image=image_File)
            static_image_path = os.path.join(settings.MEDIA_ROOT,image_File.name)
            with open(static_image_path, 'wb') as f:
                for chunks in image_File.chunks():
                    f.write(chunks)
            if not os.path.exists(static_image_path):
                return Response({'messages':'static image is not found'}, status= status.HTTP_404_NOT_FOUND)


            with open(static_image_path, 'rb') as f:
                files = {'photo': (os.path.basename(static_image_path), f, 'image/jpeg')}
                headers = {
                    'X-Token': settings.API_KEY,
                    'accept': 'application/json'
                }
                try:
                    response = requests.post(settings.API_URL, files=files, headers=headers, params={'style': 'kenga'})
                    response.raise_for_status()
                    response_data = response.json()
                    if response_data.get('ok'):
                    
                        avatar_url = response_data['face']['url']
                        
                        try:
                            avatar_response = requests.get(avatar_url)
                            if avatar_response.status_code == 200:
                                avatar_image = Image.open(BytesIO(avatar_response.content))
                                png_image_name = os.path.splitext(os.path.basename(static_image_path))[0] + ".png"
                                png_image_path = os.path.join(settings.MEDIA_ROOT, png_image_name)
                                avatar_image.save(png_image_path, format="PNG")
                                image_url = f"{request.build_absolute_uri(settings.MEDIA_URL)}/{png_image_path}"

                                
                                
                                image_instance.png_image = f'{png_image_name}'
                                image_instance.avatar_image_url = avatar_url
                                image_instance.save()

                                return Response({'data':{
                                    'message': 'Image and Avatar updated successfully',
                                    'image': AvatarImageSerailizer(image_instance).data,
                                    'png_image_path': image_url
                                }}, status=status.HTTP_200_OK)

                            else:
                                return Response({'message': 'Failed to download avatar image'}, status=status.HTTP_400_BAD_REQUEST)

                        except requests.exceptions.RequestException as e:
                            return Response({'message': 'Error downloading avatar image', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    else:
                        return Response({'msg': 'Error from external API'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except requests.exceptions.RequestException as e:
                    return Response({'msg': 'Request error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'errors':AvatarImageSerailizer.errors}, status = status.HTTP_400_BAD_REQUEST)

class UploadEyeImagesView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EyeImageSerailzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SunglassView(APIView):

    def post(self, request):
        serializer = SunglassImageSerailzer(data=request.data)
        
        if serializer.is_valid():
            avatar_url = serializer.validated_data.get('avatar_url')
            sunglasses_url = serializer.validated_data.get('sunglasses_url')

            avatar_response = requests.get(avatar_url)
            if avatar_response.status_code != 200:
                return Response({"error": "Failed to retrieve the avatar image."}, status=status.HTTP_400_BAD_REQUEST)

            sunglasses_response = requests.get(sunglasses_url)
            if sunglasses_response.status_code != 200:
                return Response({"error": "Failed to retrieve the sunglasses image."}, status=status.HTTP_400_BAD_REQUEST)

            avatar_img = cv2.imdecode(np.frombuffer(avatar_response.content, np.uint8), cv2.IMREAD_COLOR)

            sunglasses_img = cv2.imdecode(np.frombuffer(sunglasses_response.content, np.uint8), cv2.IMREAD_UNCHANGED)

            if sunglasses_img is None:
                return Response({"error": "Failed to process sunglasses image."}, status=status.HTTP_400_BAD_REQUEST)

            gray = cv2.cvtColor(avatar_img, cv2.COLOR_BGR2GRAY)

            faces = detector(gray)

            if len(faces) > 0:
                for face in faces:
                    landmarks = predictor(gray, face)
                    left_eye_pts = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
                    right_eye_pts = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]
                    left_eye_center = np.mean(left_eye_pts, axis=0).astype(int)
                    right_eye_center = np.mean(right_eye_pts, axis=0).astype(int)
                    eye_width = right_eye_center[0] - left_eye_center[0]
                    sunglasses_width = eye_width * 2
                    y_offset = left_eye_center[1] - int(sunglasses_img.shape[0] * 0.3)  # Adjust vertical positioning
                    x_offset = left_eye_center[0] - int(sunglasses_width * 0.25)    # Adjust horizontal positioning
                    overlay_image_alpha(avatar_img, sunglasses_img, x_offset, y_offset, (sunglasses_width, sunglasses_img.shape[0]))
                saved_image_path = os.path.join(settings.MEDIA_ROOT, 'modified_image.png')
                cv2.imwrite(saved_image_path, avatar_img)  # Save the modified image
                image_url = f"{request.build_absolute_uri(settings.MEDIA_URL)}modified_image.png"

                return Response({"message": "Image saved successfully.", "saved_image_path": image_url})
            else:
                return Response({"error": "No faces detected."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    


