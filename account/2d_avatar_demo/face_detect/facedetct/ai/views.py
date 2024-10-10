# views.py

import cv2
import dlib
import numpy as np
import os
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Avatar
from .serailizer import AvatarSerializer

# Load dlib detector and predictor
detector = dlib.get_frontal_face_detector()
predictor_path = "/Users/supriya/Downloads/shape_predictor_68_face_landmarks.dat"  # Update this path
predictor = dlib.shape_predictor(predictor_path)

# Function to overlay sunglasses
def overlay_image_alpha(img, overlay, x, y, overlay_size):
    overlay = cv2.resize(overlay, overlay_size)

    b, g, r, a = cv2.split(overlay)
    overlay_rgb = cv2.merge((b, g, r))

    mask = a / 255.0
    for c in range(0, 3):
        img[y:y + overlay.shape[0], x:x + overlay.shape[1], c] = \
            img[y:y + overlay.shape[0], x:x + overlay.shape[1], c] * (1.0 - mask) + overlay_rgb[:, :, c] * mask

@api_view(['POST'])
def upload_avatar(request):
    serializer = AvatarSerializer(data=request.data)
    if serializer.is_valid():
        # Save the URL and sunglasses image path to the database
        avatar_instance = serializer.save()

        # Get the avatar URL from the serializer
        avatar_url = avatar_instance.avatar_url
        
        # Download the avatar image
        response = requests.get(avatar_url)
        
        if response.status_code != 200:
            return Response({"error": "Failed to retrieve the avatar image."}, status=400)

        # Convert the image data to an OpenCV format
        avatar_img = cv2.imdecode(np.frombuffer(response.content, np.uint8), cv2.IMREAD_COLOR)

        # Load the sunglasses image
        sunglasses_path = avatar_instance.sunglasses_image.path  # Get the uploaded sunglasses path
        sunglasses = cv2.imread(sunglasses_path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel

        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(avatar_img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = detector(gray)

        if len(faces) > 0:
            for face in faces:
                landmarks = predictor(gray, face)

                # Extract coordinates for left and right eye
                left_eye_pts = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]
                right_eye_pts = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]

                # Calculate the bounding box for sunglasses based on eye coordinates
                left_eye_center = np.mean(left_eye_pts, axis=0).astype(int)
                right_eye_center = np.mean(right_eye_pts, axis=0).astype(int)
                
                # Determine the width of the sunglasses based on the distance between the eyes
                eye_width = right_eye_center[0] - left_eye_center[0]
                sunglasses_width = eye_width * 2  # Adjust as needed for the size of the sunglasses

                # Calculate the position to place the sunglasses
                y_offset = left_eye_center[1] - int(sunglasses.shape[0] * 0.3)  # Adjust vertical positioning
                x_offset = left_eye_center[0] - int(sunglasses_width * 0.25)    # Adjust horizontal positioning

                # Overlay the sunglasses on the image
                overlay_image_alpha(avatar_img, sunglasses, x_offset, y_offset, (sunglasses_width, sunglasses.shape[0]))

            # Save the modified image
            saved_image_path = os.path.join(settings.MEDIA_ROOT, 'modified_image.png')
            cv2.imwrite(saved_image_path, avatar_img)  # Save the modified image

            image_url = f"{request.build_absolute_uri(settings.MEDIA_URL)}modified_image.png"

            return Response({"message": "Image saved successfully.", "saved_image_path": image_url})
        else:
            return Response({"error": "No faces detected."}, status=400)
    return Response(serializer.errors, status=400)

import os
from django.conf import settings
from django.http import JsonResponse

class AvatarUploadView(api_view):

    def post(self, request):
        # Assuming you have the sunglasses image in the directory:
        sunglasses_file_name = 'sunglasses1.png'
        sunglasses_path = os.path.join(settings.MEDIA_ROOT, 'images', sunglasses_file_name)

        # Check if the sunglasses image exists
        if not os.path.exists(sunglasses_path):
            return JsonResponse({"error": "Sunglasses image not found."}, status=404)

        # Generate the sunglasses image URL
        sunglasses_url = f"{request.build_absolute_uri(settings.MEDIA_URL)}images/{sunglasses_file_name}"

        # You can now use this URL for further processing or send it to the frontend
        return JsonResponse({"sunglasses_url": sunglasses_url})
