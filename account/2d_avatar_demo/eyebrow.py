import cv2
import dlib
import numpy as np

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("/Users/supriya/Downloads/shape_predictor_68_face_landmarks.dat")

# Load the image
img = cv2.imread("/Users/supriya/Desktop/Screenshot 2024-09-09 at 12.27.24 PM.png")

# Load the eyebrow image (ensure it has an alpha channel for transparency)
eyebrow_img = cv2.imread("/Users/supriya/Downloads/eyebrow (1).png", cv2.IMREAD_UNCHANGED)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = detector(gray)

def overlay_image(src_img, overlay_img, position, angle):
    x_min, y_min, x_max, y_max = position
    overlay_width = x_max - x_min
    overlay_height = y_max - y_min
    resized_overlay = cv2.resize(overlay_img, (overlay_width, overlay_height))

    # Create a mask from the alpha channel if available
    if resized_overlay.shape[2] == 4:
        alpha_channel = resized_overlay[:, :, 3] / 255.0
        overlay_rgb = resized_overlay[:, :, :3]
    else:
        alpha_channel = np.ones((resized_overlay.shape[0], resized_overlay.shape[1]))
        overlay_rgb = resized_overlay

    # Rotate the overlay image
    (h, w) = overlay_rgb.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    rotated_overlay = cv2.warpAffine(overlay_rgb, M, (w, h))

    # Extract the region of interest (ROI) in the original image
    roi = src_img[y_min:y_max, x_min:x_max]

    # Ensure the ROI and overlay have the same type
    roi = roi.astype(float)
    rotated_overlay = rotated_overlay.astype(float)

    # Blend the images
    for c in range(3):
        roi[:, :, c] = roi[:, :, c] * (1 - alpha_channel) + rotated_overlay[:, :, c] * alpha_channel

    # Place the updated ROI back into the original image
    src_img[y_min:y_max, x_min:x_max] = roi.astype(np.uint8)

def get_bounding_box(landmarks):
    x_min = min(p.x for p in landmarks)
    x_max = max(p.x for p in landmarks)
    y_min = min(p.y for p in landmarks)
    y_max = max(p.y for p in landmarks)
    return (x_min, y_min, x_max, y_max)

def get_angle(landmarks):
    x1, y1 = landmarks[0].x, landmarks[0].y
    x2, y2 = landmarks[-1].x, landmarks[-1].y
    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
    return angle

def split_eyebrow_image(eyebrow_img):
    h, w = eyebrow_img.shape[:2]
    # Assuming eyebrows are placed side-by-side
    left_eyebrow = eyebrow_img[:, :w // 2]
    right_eyebrow = eyebrow_img[:, w // 2:]
    return left_eyebrow, right_eyebrow

# Split the eyebrow image into left and right eyebrows
left_eyebrow_img, right_eyebrow_img = split_eyebrow_image(eyebrow_img)

# Loop through the detected faces
for face in faces:
    # Get the facial landmarks
    landmarks = predictor(gray, face)

    # Extract eyebrow landmarks
    left_eyebrow_landmarks = [landmarks.part(n) for n in range(17, 22)]
    right_eyebrow_landmarks = [landmarks.part(n) for n in range(22, 27)]

    # Define positions and angles for both eyebrows
    left_bbox = get_bounding_box(left_eyebrow_landmarks)
    right_bbox = get_bounding_box(right_eyebrow_landmarks)
    left_angle = get_angle(left_eyebrow_landmarks)
    right_angle = get_angle(right_eyebrow_landmarks)

    # Overlay the eyebrow image on both eyebrows
    # ... (rest of the code remains the same)

# Overlay the eyebrow image on both eyebrows
overlay_image(img, left_eyebrow_img, left_bbox, left_angle)
overlay_image(img, right_eyebrow_img, right_bbox, right_angle)

# Display the output
cv2.imshow('Eyebrow Replacement', img)
cv2.waitKey(0)
cv2.destroyAllWindows()