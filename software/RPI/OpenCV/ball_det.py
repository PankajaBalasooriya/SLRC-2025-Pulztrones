import cv2
import numpy as np

def detect_pingpong_balls(frame):
    """
    Detect ping pong balls in the bottom part of the frame.
    Optimized for orange/yellow balls against dark backgrounds.
    Returns the original frame with annotations and ball position.
    """
    # Make a copy of the frame for drawing
    result_frame = frame.copy()
    
    # Define bottom roi  (bottom 40% of the frame)
    height, width = frame.shape[:2]
    bottom_roi_start = int(height * 0.5)  # Start from 60% down the frame
    
    # Extract the bottom region
    bottom_region = frame[bottom_roi_start:height, 0:width]
    
    # Draw a line indicating the ROI boundary
    cv2.line(result_frame, (0, bottom_roi_start), (width, bottom_roi_start), 
             (0, 255, 0), 2)
    cv2.putText(result_frame, "Detection Zone", (10, bottom_roi_start - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Convert to HSV color space for better color detection
    hsv = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2HSV)
    
    # Blur the image to reduce noise
    blurred = cv2.GaussianBlur(hsv, (7, 7), 1.5)
    
    # Define color ranges for orange/yellow ping pong balls
    # This range covers both yellow and orange colors
    lower_orange_yellow = np.array([10, 100, 100])
    upper_orange_yellow = np.array([35, 255, 255])
    
    # White ball detection
    lower_white = np.array([0, 0, 170])
    upper_white = np.array([180, 30, 255])
    
    # Create masks for each color
    orange_yellow_mask = cv2.inRange(blurred, lower_orange_yellow, upper_orange_yellow)
    white_mask = cv2.inRange(blurred, lower_white, upper_white)
    
    # Combine masks for all ball colors
    combined_mask = cv2.bitwise_or(orange_yellow_mask, white_mask)
    
    # Apply morphological operations to improve mask
    kernel = np.ones((5, 5), np.uint8)
    mask_processed = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    mask_processed = cv2.morphologyEx(mask_processed, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the masks
    contours, _ = cv2.findContours(mask_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Process ping pong balls
    ball_positions = []
    for contour in contours:
        # Calculate contour area
        area = cv2.contourArea(contour)
        
        # Filter small contours to remove noise (adjust this threshold based on your setup)
        if area < 400:
            continue
        
        # Approximate the contour to a polygon
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        # Get enclosing circle for the contour
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y) + bottom_roi_start)  # Adjust y-coordinate to full frame
        radius = int(radius)
        
        # Calculate circularity
        circularity = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
        
        # Ping pong balls should be circular (circularity close to 1)
        if 0.75 < circularity < 1.3:
            # Determine ball color
            if np.mean(orange_yellow_mask[int(y-5):int(y+5), int(x-5):int(x+5)]) > np.mean(white_mask[int(y-5):int(y+5), int(x-5):int(x+5)]):
                color_name = "Orange/Yellow"
                outline_color = (0, 165, 255)  # Orange outline
            else:
                color_name = "White"
                outline_color = (255, 0, 0)   
            
            # Draw the circle and label
            cv2.circle(result_frame, center, radius, outline_color, 2)
            
            # Add text labels
            cv2.putText(result_frame, f"{color_name} Ball", (center[0] - 50, center[1] - radius - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Draw crosshair at center for precise positioning
            cv2.line(result_frame, (center[0]-10, center[1]), (center[0]+10, center[1]), (0, 255, 0), 2)
            cv2.line(result_frame, (center[0], center[1]-10), (center[0], center[1]+10), (0, 255, 0), 2)
            
            # Display coordinates
            cv2.putText(result_frame, f"X:{center[0]} Y:{center[1]}", (center[0] - 50, center[1] + radius + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Add to ball positions
            ball_positions.append((center, radius, color_name))
    
    return result_frame, ball_positions

def main():
    # Open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    print("Ping Pong Ball Detector Running (Bottom Focus)...")
    print("Press 'q' to quit.")
    
    # Create a window that can be resized
    cv2.namedWindow("Ping Pong Ball Detector", cv2.WINDOW_NORMAL)
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break
        
        # Process the frame to detect ping pong balls
        result_frame, ball_positions = detect_pingpong_balls(frame)
        
        # Display detection status
        if ball_positions:
            status_text = f"Detected {len(ball_positions)} ball(s) in bottom region"
            
            # Get the largest ball (likely the closest one)
            largest_ball = max(ball_positions, key=lambda x: x[1])
            largest_pos = largest_ball[0]
            
            cv2.putText(result_frame, f"Main Ball: X:{largest_pos[0]} Y:{largest_pos[1]}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            status_text = "No balls detected in bottom region"
            
        cv2.putText(result_frame, status_text, (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
        
        # Display the result
        cv2.imshow("Ping Pong Ball Detector", result_frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()