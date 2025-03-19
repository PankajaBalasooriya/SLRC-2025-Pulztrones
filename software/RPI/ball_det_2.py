import cv2
import numpy as np

# Define color ranges in HSV
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])

white_lower = np.array([0, 0, 200])  # Adjusted for better white detection
white_upper = np.array([180, 40, 255])

# Start video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not found!")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret or frame is None:
        print("Warning: Failed to grab frame. Restarting...")
        cap.release()
        cap = cv2.VideoCapture(0)  # Restart the camera
        continue

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

    # Debugging: Show the mask to verify detection
    cv2.imshow("Color Mask", combined_mask)

    # Apply morphological operations to clean up noise
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # Detect contours instead of HoughCircles for robustness
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

    # Break on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

