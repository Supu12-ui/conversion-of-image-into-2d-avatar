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

# Load the lip image (ensure it has transparency)
lip_path = "/Users/supriya/Downloads/Mouth-women-10/mouth-w-5.png"  # Path to the new lip image
lips = cv2.imread(lip_path, cv2.IMREAD_UNCHANGED)

if lips is None:
    print(f"Error loading lip image from path: {lip_path}")
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

        # Extract coordinates for the lips (bottom lip: points 48-60, top lip: points 60-68)
        lip_pts = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(48, 68)]
        lip_center = np.mean(lip_pts, axis=0).astype(int)

        # Determine the width of the new lip image based on the width of the lips in the landmarks
        lip_width = landmarks.part(54).x - landmarks.part(48).x  # Distance between left and right corners of the lips
        lip_height = int(lips.shape[0] * (lip_width / lips.shape[1]))  # Maintain aspect ratio for resizing

        # Calculate the position to place the new lip image
        y_lip_offset = lip_center[1] - int(lip_height * 0.4)  # Adjust vertical positioning
        x_lip_offset = lip_center[0] - int(lip_width * 0.5)    # Adjust horizontal positioning

        # Overlay the new lip image on the original image
        overlay_image(img, lips, x_lip_offset, y_lip_offset, (lip_width, lip_height))

    # Display the image
    cv2.imshow("Image with New Lips", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No faces detected.")
