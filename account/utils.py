import cv2
import numpy as np
import requests
from PIL import Image
import mediapipe as mp

# Initialize Mediapipe Face Detection and Drawing utilities
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Load the sunglass image
SUNGLASS_IMAGE_PATH = '/Users/supriya/Downloads/glasses.png'
sunglasses = cv2.imread(SUNGLASS_IMAGE_PATH, -1)  # Load with alpha channel

def overlay_sunglasses_on_face(avatar_image_url):
    # Step 1: Fetch avatar image from URL
    response = requests.get(avatar_image_url)
    if response.status_code != 200:
        raise Exception('Failed to fetch avatar image')

    # Convert image to numpy array for OpenCV
    image_np = np.asarray(bytearray(response.content), dtype="uint8")
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Convert the image to RGB format (Mediapipe uses RGB format)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 2: Detect face and facial landmarks using Mediapipe
    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as face_mesh:
        results = face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            raise Exception("No face detected in the image")

        for face_landmarks in results.multi_face_landmarks:
            # Extract key points for eyes (using pre-defined indexes)
            left_eye_landmark = face_landmarks.landmark[33]  # Example index for left eye
            right_eye_landmark = face_landmarks.landmark[263]  # Example index for right eye

            # Convert normalized landmarks to pixel coordinates
            h, w, _ = image.shape
            left_eye = (int(left_eye_landmark.x * w), int(left_eye_landmark.y * h))
            right_eye = (int(right_eye_landmark.x * w), int(right_eye_landmark.y * h))

            # Step 3: Calculate sunglass position and resize the sunglass image
            sunglass_width = int(np.linalg.norm(np.array(left_eye) - np.array(right_eye)))  # Distance between eyes
            sunglass_height = int(sunglass_width * 0.4)  # Adjust height proportionally

            resized_sunglasses = cv2.resize(sunglasses, (sunglass_width, sunglass_height))

            # Calculate position for the sunglass image overlay (centered on eyes)
            x_offset = left_eye[0] - sunglass_width // 4
            y_offset = left_eye[1] - sunglass_height // 2

            # Step 4: Overlay the sunglasses on the image
            for i in range(resized_sunglasses.shape[0]):
                for j in range(resized_sunglasses.shape[1]):
                    if resized_sunglasses[i, j][3] != 0:  # Check alpha channel (transparency)
                        image[y_offset + i, x_offset + j] = resized_sunglasses[i, j][:3]

            # Step 5: Save the image with sunglasses
            output_path = 'path_to_save/with_sunglasses.png'
            cv2.imwrite(output_path, image)

            return output_path  # Return the saved image path
