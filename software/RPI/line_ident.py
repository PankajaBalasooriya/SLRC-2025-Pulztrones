import cv2
import numpy as np

def detect_line_color(frame, current_position=(0, 0), direction='right'):
    """
    Detect the color of the line in the next grid box from a webcam frame.
    
    Parameters:
    frame: Current webcam frame
    current_position (tuple): Current position (row, col) in grid
    direction (str): Direction to check ('right', 'left', 'up', 'down')
    
    Returns:
    str: Color of the line ('white', 'green', or 'unknown')
    """
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color ranges
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([90, 255, 255])
    
    lower_white = np.array([0, 0, 150])
    upper_white = np.array([180, 30, 255])
    
    # Create masks
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Get image dimensions
    height, width = frame.shape[:2]
    
    # Estimate cell size (assuming uniform grid)
    cell_size = min(height, width) // 4  # Adjust based on your grid size
    
    # Calculate next position based on current position and direction
    next_row, next_col = current_position
    if direction == 'right':
        next_col += 1
    elif direction == 'left':
        next_col -= 1
    elif direction == 'up':
        next_row -= 1
    elif direction == 'down':
        next_row += 1
    
    # Calculate region to check for line color
    x1 = next_col * cell_size
    y1 = next_row * cell_size
    x2 = (next_col + 1) * cell_size
    y2 = (next_row + 1) * cell_size
    
    # Check if next position is within frame bounds
    if x1 < 0 or y1 < 0 or x2 > width or y2 > height:
        return "outside grid"
    
    # Check color in ROI (Region of Interest)
    green_pixels = cv2.countNonZero(green_mask[y1:y2, x1:x2])
    white_pixels = cv2.countNonZero(white_mask[y1:y2, x1:x2])
    
    # For debugging, you can visualize the masks
    # cv2.imshow("Green Mask", green_mask)
    # cv2.imshow("White Mask", white_mask)
    
    # Determine dominant color (with threshold for minimum pixels to count)
    if green_pixels > white_pixels and green_pixels > 100:
        return "green"
    elif white_pixels > 100:
        return "white"
    else:
        return "unknown"

def real_time_color_detection():
    """
    Process webcam feed in real-time to detect line colors
    """
    cap = cv2.VideoCapture(0)  # Use 0 for default webcam, or specify device index
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set initial position and direction
    current_position = (1, 1)  # Starting at row 1, col 1
    direction = 'right'        # Initial direction
    
    # Create window and trackbars for adjusting position
    cv2.namedWindow("Line Color Detection")
    cv2.createTrackbar("Row", "Line Color Detection", current_position[0], 5, lambda x: None)
    cv2.createTrackbar("Col", "Line Color Detection", current_position[1], 5, lambda x: None)
    
    # Direction control buttons (using keyboard)
    direction_keys = {
        ord('w'): 'up',
        ord('a'): 'left', 
        ord('s'): 'down', 
        ord('d'): 'right'
    }
    
    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Get current position from trackbars
        current_position = (
            cv2.getTrackbarPos("Row", "Line Color Detection"),
            cv2.getTrackbarPos("Col", "Line Color Detection")
        )
        
        # Detect line color in next box
        color = detect_line_color(frame, current_position, direction)
        
        # Draw visualization on frame
        height, width = frame.shape[:2]
        cell_size = min(height, width) // 4  # Adjust based on your grid
        
        # Draw grid lines for visualization
        for i in range(1, 4):
            cv2.line(frame, (0, i * cell_size), (width, i * cell_size), (100, 100, 100), 1)
            cv2.line(frame, (i * cell_size, 0), (i * cell_size, height), (100, 100, 100), 1)
        
        # Highlight current position
        curr_row, curr_col = current_position
        cv2.rectangle(frame, 
                     (curr_col * cell_size, curr_row * cell_size), 
                     ((curr_col + 1) * cell_size, (curr_row + 1) * cell_size), 
                     (0, 0, 255), 2)
        
        # Calculate and highlight next position
        next_row, next_col = current_position
        if direction == 'right':
            next_col += 1
        elif direction == 'left':
            next_col -= 1
        elif direction == 'up':
            next_row -= 1
        elif direction == 'down':
            next_row += 1
            
        # Only draw next position if it's within frame bounds
        if (0 <= next_row < height // cell_size and 0 <= next_col < width // cell_size):
            cv2.rectangle(frame, 
                         (next_col * cell_size, next_row * cell_size), 
                         ((next_col + 1) * cell_size, (next_row + 1) * cell_size), 
                         (255, 0, 0), 2)
        
        # Display the detected color 
        text = f"Detected Color: {color}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, f"Direction: {direction}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, "Press W/A/S/D to change direction", (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Display the frame
        cv2.imshow("Line Color Detection", frame)
        
        # Handle key presses for direction control
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key in direction_keys:
            direction = direction_keys[key]
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    real_time_color_detection()