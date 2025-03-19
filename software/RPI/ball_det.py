import cv2
import numpy as np

# Define color ranges in HSV
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])

white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 50, 255])

# Open the camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Warning: Frame not captured. Retrying...")
        continue  # Skip this frame instead of breaking

    height, width, _ = frame.shape

    # Define ROI (lower 40% of the frame)
    roi_top = int(height * 0.6)
    roi = frame[roi_top:, :]

    # Convert ROI to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Create masks for yellow and white
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_white = cv2.inRange(hsv, white_lower, white_upper)

    # Combine both masks
    combined_mask = mask_yellow + mask_white

    # Debug: Show the mask window to check if the ball is detected
    cv2.imshow("Color Mask", combined_mask)

    # Apply morphological operations to clean up noise
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # Try Hough Circle Detection
    circles = cv2.HoughCircles(combined_mask, cv2.HOUGH_GRADIENT, dp=1.5, minDist=20,
                               param1=50, param2=20, minRadius=10, maxRadius=60)

    detected = False  # Flag to check if a ball was detected

    if circles is not None and len(circles) > 0:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cx, cy, radius = i[0], i[1], i[2]

            abs_cy = roi_top + cy  # Convert ROI y to full frame y

            # Determine color by checking the pixel value at the center
            hsv_value = hsv[cy, cx]
            hue = hsv_value[0]

            ball_color = "Yellow" if 20 <= hue <= 30 else "White"

            # Draw detected circle
            cv2.circle(frame, (cx, abs_cy), radius, (0, 255, 0), 2)
            cv2.putText(frame, ball_color, (cx - 20, abs_cy - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            detected = True  # Ball was detected

    # Backup: If no circle was detected, use contour detection
    if not detected:
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours is None:
            contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Filter out small noise
                x, y, w, h = cv2.boundingRect(cnt)
                center_x, center_y = x + w // 2, y + h // 2
                abs_y = roi_top + y  # Convert ROI y to full frame y

                # Determine color
                mask_roi = hsv[y:y+h, x:x+w]
                avg_hue = np.mean(mask_roi[:, :, 0])  # Average hue in ROI

                ball_color = "Yellow" if 20 <= avg_hue <= 30 else "White"

                # Draw rectangle and label
                cv2.rectangle(frame, (x, abs_y), (x + w, abs_y + h), (0, 255, 0), 2)
                cv2.putText(frame, ball_color, (x, abs_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Draw ROI boundary
    cv2.line(frame, (0, roi_top), (width, roi_top), (255, 0, 0), 2)

    # Show frame
    cv2.imshow("Enhanced Ball Detection", frame)

    # Break on 'q' or 'Esc' key
    key = cv2.waitKey(1)
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
