import cv2
import numpy as np

def detect_adjacent_line_color(frame):
    """
    Detect the color of the line adjacent to the robot's current position
    using edge detection to first identify the line and then analyze its color.
    Returns: The detected color (0 for white, 1 for green, 2 for unknown)
    """
    # Get image dimensions
    height, width = frame.shape[:2]
    
    # Define initial region to look for lines (bottom half of the frame)
    roi_y = height // 2
    roi_height = height // 2
    roi_x = width // 4
    roi_width = width // 2
    
    # Create region of interest
    roi = frame[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    
    # Convert to grayscale for edge detection
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    
    # Use Canny edge detection to find edges
    edges = cv2.Canny(blurred_roi, 50, 150)
    
    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)
    
    # Create a visualization frame for debugging
    debug_frame = frame.copy()
    cv2.rectangle(debug_frame, (roi_x, roi_y), (roi_x+roi_width, roi_y+roi_height), (0, 255, 255), 2)
    
    # If no lines detected, return unknown
    if lines is None:
        cv2.putText(debug_frame, "No lines detected", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return 2, debug_frame
    
    # Find the most prominent line
    max_line_length = 0
    best_line = None
    
    for line in lines:
        x1, y1, x2, y2 = line[0]
        line_length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        
        if line_length > max_line_length:
            max_line_length = line_length
            best_line = line[0]
    
    # Extract the best line coordinates
    x1, y1, x2, y2 = best_line
    
    # Convert back to full frame coordinates
    x1 += roi_x
    x2 += roi_x
    y1 += roi_y
    y2 += roi_y
    
    # Draw the detected line on the frame for visualization
    cv2.line(debug_frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
    # Calculate line angle to determine orientation
    angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
    
    # Create a tight ROI around the detected line
    # Calculate the midpoint of the line
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    
    # Define ROI width and height based on line orientation
    line_roi_width = max(50, abs(x2 - x1) // 2)
    line_roi_height = max(50, abs(y2 - y1) // 2)
    
    # Create tight ROI coordinates, ensuring they stay within frame boundaries
    line_roi_x = max(0, mid_x - line_roi_width // 2)
    line_roi_y = max(0, mid_y - line_roi_height // 2)
    line_roi_width = min(width - line_roi_x, line_roi_width)
    line_roi_height = min(height - line_roi_y, line_roi_height)
    
    # Draw the line-specific ROI
    cv2.rectangle(debug_frame, 
                 (line_roi_x, line_roi_y), 
                 (line_roi_x + line_roi_width, line_roi_y + line_roi_height), 
                 (255, 0, 0), 2)
    
    # Extract the line ROI
    line_roi = frame[line_roi_y:line_roi_y + line_roi_height, 
                     line_roi_x:line_roi_x + line_roi_width]
    
    # Convert line ROI to HSV for color detection
    hsv = cv2.cvtColor(line_roi, cv2.COLOR_BGR2HSV)
    
    # Improved color ranges for detection in dark backgrounds
    # Adjusted to better distinguish white from green in varying lighting
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    
    # Expanded white range with lower saturation and value thresholds
    lower_white = np.array([0, 0, 120])
    upper_white = np.array([180, 50, 255])
    
    # Create color masks
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Count pixels of each color in the line ROI
    green_pixels = cv2.countNonZero(green_mask)
    white_pixels = cv2.countNonZero(white_mask)
    
    # Calculate percentage of colored pixels in ROI
    total_roi_pixels = line_roi_width * line_roi_height
    if total_roi_pixels == 0:  # Safety check
        return 2, debug_frame
        
    green_percentage = green_pixels / total_roi_pixels * 100
    white_percentage = white_pixels / total_roi_pixels * 100
    
    # Display percentages on the frame for debugging
    cv2.putText(debug_frame, f"White: {white_percentage:.1f}%", 
               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(debug_frame, f"Green: {green_percentage:.1f}%", 
               (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Determine color with minimum threshold percentage and bias toward white detection
    # The bias helps in dark environments where white might appear differently
    threshold_percentage = 5  # Minimum percentage to consider a valid detection
    
    color = 2  # Default: unknown
    
    # Give slight preference to white detection in ambiguous cases
    if white_percentage > threshold_percentage and white_percentage >= green_percentage * 0.8:
        color = 0  # White
    elif green_percentage > threshold_percentage and green_percentage > white_percentage * 1.2:
        color = 1  # Green
    
    return color, debug_frame

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
        
        # Map color code to string for display
        color_name = "Unknown"
        if color == 0:
            color_name = "White"
        elif color == 1:
            color_name = "Green"
        
        # Display result on frame
        cv2.putText(marked_frame, f"Detected Color: {color_name}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, (0, 0, 255), 2)
        
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