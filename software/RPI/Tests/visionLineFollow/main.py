import cv2
import numpy as np

# Initialize webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

# Set resolution for the webcam
cap.set(3, 640)  # Width
cap.set(4, 360)  # Height

# Create a kernel for erosion and dilation
kernel = np.ones((3, 3), np.uint8)

while True:
    # Capture frame-by-frame
    ret, image = cap.read()
    
    if not ret:
        print("Failed to grab frame")
        break

    roi = image[200:250, 0:639]
    
    Blackline = cv2.inRange(roi, (0, 0, 0), (50, 50, 50))

    kernal = np.ones((3,3), np.uint8)

    Blackline = cv2.erode(Blackline, kernal, iterations=10)
    Blackline = cv2.dilate(Blackline, kernal, iterations=10)


    contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(image, contours, -1, (0, 255, 0), 0)

    if len(contours) > 0 :
        x,y,w,h = cv2.boundingRect(contours[0])	   
        #cv2.rectangle(image, (x, y), (x+w,y+h), (0,0,255),3)
        cv2.line(image, (int(x + w / 2), 0), (int(x + w / 2), 360), (255, 0, 0), 3)



    #cv2.imshow("Black in range", Blackline)
    #cv2.imshow("Camera", image)
    cv2.imshow("Original with Contours", image)

    # Check if the user pressed 'q' to quit
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# Release the webcam and close any open windows
cap.release()
cv2.destroyAllWindows()
