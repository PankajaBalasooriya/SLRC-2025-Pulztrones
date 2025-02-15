import cv2

# Open the default camera (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        print("Failed to capture image")
        break

    cv2.imshow("Webcam Test", frame)  # Display the frame

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()