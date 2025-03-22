import cv2
import numpy as np

def detect_ball_color(frame, params=None):
    """
    Detect a ball in a single frame and return the marked frame and ball information.
    
    Args:
        frame: Input image frame (BGR format)
        params: Dictionary of detection parameters. If None, default parameters will be used.
            Possible keys:
            - h_min, h_max, s_min, s_max, v_min, v_max: HSV thresholds for white ball
            - min_circularity: Minimum circularity value (0-1)
            - min_radius, max_radius: Size constraints for detected balls
            - top_line_percent, left_margin_percent, right_margin_percent: ROI boundaries
    
    Returns:
        tuple: (marked_frame, ball_info)
            - marked_frame: Original frame with detection visualization
            - ball_info: Dictionary with ball data or None if no ball detected
    """
    
    
    # Default parameters if none provided
    if params is None:
        params = {
            'h_min': 0, 'h_max': 80, 
            's_min': 0, 's_max': 80, 
            'v_min': 150, 'v_max': 255,
            'min_circularity': 0.6,
            'min_radius': 15, 'max_radius': 100,
            'top_line_percent': 55,
            'left_margin_percent': 15,
            'right_margin_percent': 15
        }
    
    # Extract parameters
    h_min = params.get('h_min', 0)
    h_max = params.get('h_max', 80)
    s_min = params.get('s_min', 0)
    s_max = params.get('s_max', 80)
    v_min = params.get('v_min', 150)
    v_max = params.get('v_max', 255)
    min_circularity = params.get('min_circularity', 0.6)
    min_radius = params.get('min_radius', 15)
    max_radius = params.get('max_radius', 100)
    top_line_percent = params.get('top_line_percent', 55)
    left_margin_percent = params.get('left_margin_percent', 15)
    right_margin_percent = params.get('right_margin_percent', 15)
    
    # Make a copy for display
    display_frame = frame.copy()
    
    # Define the custom region of interest (ROI)
    height, width = frame.shape[:2]
    
    # Calculate ROI boundaries
    top_boundary = int(height * (top_line_percent / 100.0))
    left_boundary = int(width * (left_margin_percent / 100.0))
    right_boundary = width - int(width * (right_margin_percent / 100.0))
    
    # Create a mask for the custom ROI
    roi_mask = np.zeros((height, width), dtype=np.uint8)
    
    # Define ROI polygon points (trapezoid shape)
    roi_points = np.array([
        [left_boundary, top_boundary],     # Top left
        [right_boundary, top_boundary],    # Top right
        [width - 10, height - 10],         # Bottom right
        [10, height - 10]                  # Bottom left
    ], np.int32)
    
    # Fill the ROI polygon
    cv2.fillPoly(roi_mask, [roi_points], 255)
    
    # Apply the ROI mask to the frame
    roi = cv2.bitwise_and(frame, frame, mask=roi_mask)
    
    # Convert to HSV color space
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    
    # Define color ranges (HSV)
    # White/cream ball with parameters
    white_lower = np.array([h_min, s_min, v_min])
    white_upper = np.array([h_max, s_max, v_max])
    
    # Orange-yellow ball
    orange_yellow_lower = np.array([15, 100, 100])
    orange_yellow_upper = np.array([35, 255, 255])
    
    # Create masks for each color
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    orange_yellow_mask = cv2.inRange(hsv, orange_yellow_lower, orange_yellow_upper)
    
    # Combine masks
    combined_mask = cv2.bitwise_or(white_mask, orange_yellow_mask)
    
    # Noise removal with morphological operations
    kernel = np.ones((5, 5), np.uint8)
    processed_mask = cv2.erode(combined_mask, kernel, iterations=1)
    processed_mask = cv2.dilate(processed_mask, kernel, iterations=2)
    
    # Find contours
    contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Best ball candidate
    best_ball = None
    best_score = 0  # Higher score means better ball candidate
    
    # Process contours to find the best ball
    for contour in contours:
        # Calculate area
        area = cv2.contourArea(contour)
        if area < 100:  # Minimal area filtering
            continue
            
        # Calculate circularity - perfect circle has value of 1
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        
        # Get bounding circle
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        
        # Make sure center is within our ROI
        if roi_mask[center[1], center[0]] == 0:
            continue
        
        # Basic filtering
        if radius < min_radius or radius > max_radius:
            continue
        if circularity < min_circularity:
            continue
            
        # Calculate a score based on circularity and being in the lower part of the image
        position_score = y / height  # 0 to 1, higher means lower in image
        circle_score = circularity  # 0 to 1, higher means more circular
        
        # Combined score: weight circularity more heavily
        score = circle_score * 0.7 + position_score * 0.3
        
        # If this is the best ball candidate so far, save it
        if score > best_score:
            best_score = score
            
            # Determine the color
            mask = np.zeros_like(combined_mask)
            cv2.drawContours(mask, [contour], 0, 255, -1)
            
            orange_yellow_pixels = cv2.countNonZero(cv2.bitwise_and(orange_yellow_mask, mask))
            white_pixels = cv2.countNonZero(cv2.bitwise_and(white_mask, mask))
            
            if orange_yellow_pixels > white_pixels:
                color = "Orange-Yellow"
                display_color = (0, 165, 255)  # BGR orange
            else:
                color = "White"
                display_color = (255, 255, 255)  # BGR white
            
            radius = int(radius)
            
            best_ball = {
                "color": color,
                "center": center,
                "radius": radius,
                "display_color": display_color,
                "score": score,
                "circularity": circularity
            }
    
    # If no ball found with contours, try Hough circles as a backup
    if best_ball is None:
        # Convert the masked frame to grayscale for HoughCircles
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        
        # Detect circles
        circles = cv2.HoughCircles(
            gray_blurred,
            cv2.HOUGH_GRADIENT,
            dp=1,
            minDist=50,
            param1=50,
            param2=30,
            minRadius=min_radius,
            maxRadius=max_radius
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            
            # Find the best circle (most in the lower part of the image)
            best_y = 0
            best_circle = None
            
            for circle in circles[0, :]:
                x, y, r = circle
                
                # Make sure center is within our ROI
                if y < height and x < width and roi_mask[y, x] == 0:
                    continue
                    
                if y > best_y:
                    best_y = y
                    best_circle = circle
            
            if best_circle is not None:
                x, y, r = best_circle
                
                # Create a mask for the circle
                circle_mask = np.zeros_like(combined_mask)
                cv2.circle(circle_mask, (x, y), r, 255, -1)
                
                # Determine the color
                orange_yellow_pixels = cv2.countNonZero(cv2.bitwise_and(orange_yellow_mask, circle_mask))
                white_pixels = cv2.countNonZero(cv2.bitwise_and(white_mask, circle_mask))
                
                if orange_yellow_pixels > white_pixels:
                    color = "Orange-Yellow"
                    display_color = (0, 165, 255)  # BGR orange
                else:
                    color = "White"
                    display_color = (255, 255, 255)  # BGR white
                
                center = (int(x), int(y))
                
                best_ball = {
                    "color": color,
                    "center": center,
                    "radius": r,
                    "display_color": display_color,
                    "score": 0.8,  # Default score for Hough circles
                    "circularity": 0.9  # Assume high circularity since it's from HoughCircles
                }
    
    # Draw ROI boundary (red polygon)
    cv2.polylines(display_frame, [roi_points], True, (0, 0, 255), 2)
    
    # Ball detection result
    if best_ball:
        # Draw the circle on the display frame
        cv2.circle(display_frame, best_ball["center"], best_ball["radius"], best_ball["display_color"], 2)
        cv2.putText(display_frame, best_ball["color"], 
                  (best_ball["center"][0] - 40, best_ball["center"][1] - best_ball["radius"] - 10),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, best_ball["display_color"], 2)
        
        # Add ball detection info
        cv2.putText(display_frame, "Ball detected", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        # No ball detected
        cv2.putText(display_frame, "No ball detected", (10, 30),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    return display_frame, best_ball




def main():
    # Load your parameters once (or use the defaults by passing None)
    detection_params = {
        'h_min': 0, 'h_max': 80, 
        's_min': 0, 's_max': 80, 
        'v_min': 150, 'v_max': 255,
        'min_circularity': 0.6,
        'min_radius': 15, 'max_radius': 100,
        'top_line_percent': 55,
        'left_margin_percent': 15,
        'right_margin_percent': 15
    }

    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process the frame to detect the ball
        marked_frame, ball_info = detect_ball_color(frame, detection_params)
        
        # Display the result
        cv2.imshow('Ball Detection', marked_frame)
        
        # If a ball was detected, you can use its information
        if ball_info:
            print(f"Ball color: {ball_info['color']}")
            print(f"Position: {ball_info['center']}")
        
        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()