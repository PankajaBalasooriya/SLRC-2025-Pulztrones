import cv2
import numpy as np

def detect_adjacent_line_color(frame):
    """
    Detect the color of the line adjacent to the robot's current position
    Returns: The detected color ('green', 'white', or 'unknown')
    """
    # Convert frame to HSV color space for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color ranges
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([90, 255, 255])
    
    lower_white = np.array([0, 0, 150])
    upper_white = np.array([180, 30, 255])
    
    # Create color masks
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Get image dimensions
    height, width = frame.shape[:2]
    
    # Define the region to analyze (bottom half of the frame)
    roi_y = height // 2
    roi_height = height // 2
    roi_x = 0
    roi_width = width
    
    # Create region of interest
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    green_roi = green_mask[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    white_roi = white_mask[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    
    # Count pixels of each color in ROI
    green_pixels = cv2.countNonZero(green_roi)
    white_pixels = cv2.countNonZero(white_roi)
    
    # Determine dominant color
    color = 2
    if green_pixels > white_pixels and green_pixels > 100:
        color = 1
    elif white_pixels > 100:
        color = 0
    
    # Draw ROI rectangle on frame for visualization
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x+roi_width, roi_y+roi_height), (0, 255, 255), 2)
    
    
    
    return color, frame

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame")
            break
        
        # Detect line color
        color, marked_frame = detect_adjacent_line_color(frame)
        
        # Display result on frame
        cv2.putText(marked_frame, f"Detected Color: {color}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow("Line Detection", marked_frame)
        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()