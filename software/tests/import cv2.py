import cv2

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam not detected. Check connection!")
else:
    # Capture one frame
    ret, frame = cap.read()
    if ret:
        cv2.imwrite('/home/pi/webcam_test.jpg', frame)
        print("Image captured: /home/pi/webcam_test.jpg")
    else:
        print("Failed to capture image")

# Release camera
cap.release()
