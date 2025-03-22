import cv2

# Open a connection to the webcam (0 is the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()

# Capture a single frame
ret, frame = cap.read()

if ret:
    # Save the image
    cv2.imwrite("captured_image_6.jpg", frame)
    print("Image saved as captured_image.jpg")
else:
    print("Error: Could not capture image")

# Release the camera
cap.release()
cv2.destroyAllWindows()
