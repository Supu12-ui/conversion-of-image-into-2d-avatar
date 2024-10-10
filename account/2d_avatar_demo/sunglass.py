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

# Load the sunglasses image (ensure the sunglasses image has transparency, e.g., PNG with alpha channel)
sunglasses_path = "/Users/supriya/Downloads/glasses.png"
sunglasses = cv2.imread(sunglasses_path, cv2.IMREAD_UNCHANGED)  # Load with alpha channel

if sunglasses is None:
    print(f"Error loading sunglasses image from path: {sunglasses_path}")
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

# Function to overlay sunglasses
def overlay_image_alpha(img, overlay, x, y, overlay_size):
    overlay = cv2.resize(overlay, overlay_size)

    b, g, r, a = cv2.split(overlay)
    overlay_rgb = cv2.merge((b, g, r))

    mask = a / 255.0
    for c in range(0, 3):
        img[y:y+overlay.shape[0], x:x+overlay.shape[1], c] = \
     img[y:y+overlay.shape[0], x:x+overlay.shape[1], c] * (1.0 - mask) + overlay_rgb[:, :, c] * mask

# Continue processing if faces are detected
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
        overlay_image_alpha(img, sunglasses, x_offset, y_offset, (sunglasses_width, sunglasses.shape[0]))

    # Display the image
    cv2.imshow("Image with Sunglasses", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No faces detected.")