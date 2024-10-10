import cv2
import dlib
import numpy as np

# Load the detector and predictor
detector = dlib.get_frontal_face_detector()
predictor_path = "/Users/supriya/Downloads/shape_predictor_68_face_landmarks.dat"
predictor = dlib.shape_predictor(predictor_path)

# Load the main image
img_path = "/Users/supriya/Desktop/Screenshot 2024-09-09 at 12.27.24 PM.png"
img = cv2.imread(img_path)

# Load the left and right eye images with alpha channel
left_eye_img_path = "/Users/supriya/Downloads/eye-women-left-5.png"
right_eye_img_path = "/Users/supriya/Downloads/eye-women-right-5.png"

left_eye_img = cv2.imread(left_eye_img_path, cv2.IMREAD_UNCHANGED)
right_eye_img = cv2.imread(right_eye_img_path, cv2.IMREAD_UNCHANGED)

# Check if images loaded successfully
if img is None or left_eye_img is None or right_eye_img is None:
    print("Error loading images.")
    exit()

# Convert to grayscale for face detection
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = detector(gray)

if len(faces) == 0:
    print("No faces detected.")
    exit()

for face in faces:
    landmarks = predictor(gray, face)

    # Process the left eye (landmarks 36 to 41)
    left_eye_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(36, 42)])
    x_min, y_min = np.min(left_eye_points, axis=0)
    x_max, y_max = np.max(left_eye_points, axis=0)

    eye_width = x_max - x_min
    eye_height = y_max - y_min

    # Resize and overlay the left eye image
    resized_left_eye_img = cv2.resize(left_eye_img, (eye_width, eye_height))

    # Calculate rotation angle for the left eye
    left_corner = landmarks.part(36).x, landmarks.part(36).y
    right_corner = landmarks.part(39).x, landmarks.part(39).y
    angle = np.degrees(np.arctan2(right_corner[1] - left_corner[1], right_corner[0] - left_corner[0]))

    # Rotate the left eye image
    M = cv2.getRotationMatrix2D((int(eye_width // 2), int(eye_height // 2)), angle, 1)
    rotated_left_eye_img = cv2.warpAffine(resized_left_eye_img, M, (eye_width, eye_height), flags=cv2.INTER_LINEAR)

    # Overlay the left eye image onto the main image
    x_offset, y_offset = x_min, y_min

    if rotated_left_eye_img.shape[2] == 4:  # Check for alpha channel
        alpha_channel = rotated_left_eye_img[:, :, 3] / 255.0
        for c in range(0, 3):
            img[y_offset:y_offset+eye_height, x_offset:x_offset+eye_width, c] = \
                rotated_left_eye_img[:, :, c] * alpha_channel + \
                img[y_offset:y_offset+eye_height, x_offset:x_offset+eye_width, c] * (1.0 - alpha_channel)

    # Process the right eye (landmarks 42 to 47)
    right_eye_points = np.array([(landmarks.part(i).x, landmarks.part(i).y) for i in range(42, 48)])
    x_min, y_min = np.min(right_eye_points, axis=0)
    x_max, y_max = np.max(right_eye_points, axis=0)

    eye_width = x_max - x_min
    eye_height = y_max - y_min

    # Resize and overlay the right eye image
    resized_right_eye_img = cv2.resize(right_eye_img, (eye_width, eye_height))

    # Calculate rotation angle for the right eye
    left_corner = landmarks.part(42).x, landmarks.part(42).y
    right_corner = landmarks.part(45).x, landmarks.part(45).y
    angle = np.degrees(np.arctan2(right_corner[1] - left_corner[1], right_corner[0] - left_corner[0]))

    # Rotate the right eye image
    M = cv2.getRotationMatrix2D((int(eye_width // 2), int(eye_height // 2)), angle, 1)
    rotated_right_eye_img = cv2.warpAffine(resized_right_eye_img, M, (eye_width, eye_height), flags=cv2.INTER_LINEAR)

    # Overlay the right eye image onto the main image
    x_offset, y_offset = x_min, y_min

    if rotated_right_eye_img.shape[2] == 4:  # Check for alpha channel
        alpha_channel = rotated_right_eye_img[:, :, 3] / 255.0
        for c in range(0, 3):
            img[y_offset:y_offset+eye_height, x_offset:x_offset+eye_width, c] = \
                rotated_right_eye_img[:, :, c] * alpha_channel + \
                img[y_offset:y_offset+eye_height, x_offset:x_offset+eye_width, c] * (1.0 - alpha_channel)

# Display the final image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()