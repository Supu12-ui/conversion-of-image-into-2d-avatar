import cv2
import dlib
import numpy as np

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor_path = "/Users/supriya/Downloads/shape_predictor_68_face_landmarks.dat"
try:
    predictor = dlib.shape_predictor(predictor_path)
except RuntimeError as e:
    print(f"Error loading predictor: {e}")
    exit()

# Load the image
img_path = "/Users/supriya/Desktop/Screenshot 2024-09-09 at 12.27.24 PM.png"
img = cv2.imread(img_path)

# Check if the image was loaded successfully
if img is None:
    print(f"Error loading image from path: {img_path}")
    exit()

# Load the hair image (ensure it has transparency)
hair_path = "/Users/supriya/Downloads/hair.png"  # Path to the new hair image
hair = cv2.imread(hair_path, cv2.IMREAD_UNCHANGED)

if hair is None:
    print(f"Error loading hair image from path: {hair_path}")
    exit()

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
try:
    faces = detector(gray)
    print(f"Detected {len(faces)} faces.")
except RuntimeError as e:
    print(f"RuntimeError during face detection: {e}")
    exit()

# Function to overlay images
def overlay_image(img, overlay, x, y, overlay_size):
    overlay = cv2.resize(overlay, overlay_size)

    if overlay.shape[2] == 4:  # Check if the overlay has an alpha channel
        b, g, r, a = cv2.split(overlay)
        overlay_rgb = cv2.merge((b, g, r))

        mask = a / 255.0
        for c in range(0, 3):
            img[y:y + overlay.shape[0], x:x + overlay.shape[1], c] = \
                img[y:y + overlay.shape[0], x:x + overlay.shape[1], c] * (1.0 - mask) + overlay_rgb[:, :, c] * mask
    else:  # If no alpha channel, just overlay without blending
        img[y:y + overlay.shape[0], x:x + overlay.shape[1]] = overlay

# Continue processing if faces are detected
if len(faces) > 0:
    for face in faces:
        landmarks = predictor(gray, face)

        # Extract coordinates for the hairline (top of the head)
        # You can customize the points based on your image and hairline position
        hairline_pts = [(landmarks.part(18).x, landmarks.part(18).y),  # Left temple
                        (landmarks.part(27).x, landmarks.part(27).y),  # Nose bottom
                        (landmarks.part(24).x, landmarks.part(24).y)]  # Right temple

        # Calculate the center of the hairline
        hairline_center = np.mean(hairline_pts, axis=0).astype(int)

        # Determine the width and height of the new hair image
        hair_width = landmarks.part(16).x - landmarks.part(0).x  # Distance between left and right temples
        hair_height = int(hair.shape[0] * (hair_width / hair.shape[1]))  # Maintain aspect ratio for resizing

        # Calculate the position to place the new hair image
        y_hair_offset = hairline_center[1] - int(hair_height * 0.8)  # Adjust vertical positioning
        x_hair_offset = hairline_center[0] - int(hair_width * 0.5)    # Adjust horizontal positioning

        # Overlay the new hair image on the original image
        overlay_image(img, hair, x_hair_offset, y_hair_offset, (hair_width, hair_height))

    # Display the image
    cv2.imshow("Image with New Hair", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No faces detected.")
