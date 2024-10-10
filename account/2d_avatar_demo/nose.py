import cv2
import dlib

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("/Users/supriya/Downloads/shape_predictor_68_face_landmarks.dat")

# Load the image
img = cv2.imread("/Users/supriya/Desktop/Screenshot 2024-09-09 at 12.27.24 PM.png")

# Load the nose image
nose_img = cv2.imread("/Users/supriya/Downloads/nose.png", cv2.IMREAD_UNCHANGED)  # Ensure it has an alpha channel

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
faces = detector(gray)

# Loop through the detected faces
for face in faces:
    # Get the facial landmarks
    landmarks = predictor(gray, face)

    # Get the nose landmarks
    nose_landmarks_x = [landmarks.part(n).x for n in range(27, 36)]
    nose_landmarks_y = [landmarks.part(n).y for n in range(27, 36)]

    # Calculate the bounding box for the nose
    x_min, x_max = min(nose_landmarks_x), max(nose_landmarks_x)
    y_min, y_max = min(nose_landmarks_y), max(nose_landmarks_y)

    # Resize the nose image to fit the detected nose region
    nose_width = x_max - x_min
    nose_height = y_max - y_min
    nose_resized = cv2.resize(nose_img, (nose_width, nose_height))

    # Get the region of interest (ROI) in the original image
    roi = img[y_min:y_max, x_min:x_max]

    # Create a mask from the nose image alpha channel
    if nose_resized.shape[2] == 4:  # Check if the nose image has an alpha channel
        alpha_channel = nose_resized[:, :, 3] / 255.0
        nose_resized = nose_resized[:, :, :3]
    else:
        alpha_channel = np.ones((nose_resized.shape[0], nose_resized.shape[1]))

    # Overlay the nose image on the ROI
    for c in range(0, 3):
        roi[:, :, c] = roi[:, :, c] * (1 - alpha_channel) + nose_resized[:, :, c] * alpha_channel

    # Place the updated ROI back into the original image
    img[y_min:y_max, x_min:x_max] = roi

# Display the image
cv2.imshow("Image with Nose Overlay", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
