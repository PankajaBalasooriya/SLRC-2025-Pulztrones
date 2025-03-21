import cv2
import numpy as np
import time
# If you're using a real robot, you'll need to import your robot control library
# For example:
# from robot_control import RobotController

class StripeFollower:
    def __init__(self):
        # Camera setup
        self.camera = cv2.VideoCapture(0)  # Use 0 for default camera, adjust if needed
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Parameters for stripe detection
        self.min_threshold = 60  # Minimum threshold for Canny edge detection
        self.max_threshold = 150  # Maximum threshold for Canny edge detection
        self.stripe_threshold = 120  # Threshold for binary image (adjust based on stripe color)
        
        # Control parameters
        self.center_offset = 0  # Offset from center (0 means perfectly centered)
        self.max_speed = 50  # Maximum speed of the robot
        self.kp = 0.5  # Proportional gain for controller
        
        # Region of interest parameters (focus on upper part of the image)
        self.roi_height = 100  # Height of region of interest
        self.roi_y_offset = 100  # Y-offset from the top of the frame
        
        # For visualization
        self.debug_mode = True
        
        # Uncomment if using an actual robot
        # self.robot = RobotController()

    def preprocess_frame(self, frame):
        """Preprocess the camera frame for stripe detection"""
        # Create region of interest (upper portion of the frame)
        height, width = frame.shape[:2]
        roi = frame[self.roi_y_offset:self.roi_y_offset+self.roi_height, 0:width]
        
        # Convert to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Create binary image to detect stripes (assuming stripes are darker than background)
        # Adjust the threshold based on your stripe color
        _, binary = cv2.threshold(blurred, self.stripe_threshold, 255, cv2.THRESH_BINARY_INV)
        
        # Apply morphological operations to clean up the binary image
        kernel = np.ones((5, 5), np.uint8)
        binary = cv2.erode(binary, kernel, iterations=1)
        binary = cv2.dilate(binary, kernel, iterations=2)
        
        # Apply Canny edge detection to find stripe edges
        edges = cv2.Canny(binary, self.min_threshold, self.max_threshold)
        
        return roi, binary, edges

    def detect_stripes(self, binary, edges):
        """Detect the two stripes and find their centers"""
        # Find contours in the binary image
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) < 2:
            return None, None, []
        
        # Filter contours by size and shape
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Minimum area threshold
                x, y, w, h = cv2.boundingRect(contour)
                # Filter for elongated shapes that are more likely to be stripes
                if h > w and h/w > 1.5:
                    valid_contours.append(contour)
        
        # Not enough valid stripes found
        if len(valid_contours) < 2:
            return None, None, valid_contours
        
        # Sort contours by x position
        sorted_contours = sorted(valid_contours, key=lambda c: cv2.boundingRect(c)[0])
        
        # Get the leftmost and rightmost stripes
        left_stripe = sorted_contours[0]
        right_stripe = sorted_contours[-1]
        
        # Calculate centers of the stripes
        left_x, left_y, left_w, left_h = cv2.boundingRect(left_stripe)
        right_x, right_y, right_w, right_h = cv2.boundingRect(right_stripe)
        
        left_center = left_x + left_w // 2
        right_center = right_x + right_w // 2
        
        return left_center, right_center, [left_stripe, right_stripe]

    def calculate_center_position(self, left_center, right_center, frame_width):
        """Calculate the ideal center position between the two stripes"""
        if left_center is None or right_center is None:
            return None
        
        # Calculate the midpoint between the two stripes
        center_x = (left_center + right_center) / 2
        
        # Calculate offset from the center of the frame
        frame_center = frame_width / 2
        self.center_offset = center_x - frame_center
        
        return center_x

    def control_robot(self):
        """Apply PID control to keep the robot centered between stripes"""
        if self.center_offset is None:
            # No stripes detected, stop or slow down
            left_speed = right_speed = 0
            return left_speed, right_speed
        
        # Calculate steering adjustment using proportional control
        steering = -self.kp * self.center_offset
        
        # Calculate left and right wheel speeds
        left_speed = self.max_speed + steering
        right_speed = self.max_speed - steering
        
        # Ensure values are within range
        left_speed = max(0, min(self.max_speed * 2, left_speed))
        right_speed = max(0, min(self.max_speed * 2, right_speed))
        
        return left_speed, right_speed

    def visualize(self, original_frame, roi, binary, left_center, right_center, center_x, stripes):
        """Create a visualization frame for debugging"""
        # Create a copy for visualization
        viz_frame = original_frame.copy()
        height, width = original_frame.shape[:2]
        roi_y_start = self.roi_y_offset
        
        # Draw region of interest
        cv2.rectangle(viz_frame, 
                     (0, roi_y_start), 
                     (width, roi_y_start + self.roi_height), 
                     (0, 255, 0), 2)
        
        # Draw stripe contours
        for contour in stripes:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(viz_frame, 
                         (x, y + roi_y_start), 
                         (x + w, y + h + roi_y_start), 
                         (0, 255, 0), 2)
            
        # Draw stripe centers
        if left_center is not None:
            cv2.circle(viz_frame, (left_center, roi_y_start + 50), 5, (255, 0, 0), -1)
        
        if right_center is not None:
            cv2.circle(viz_frame, (right_center, roi_y_start + 50), 5, (0, 0, 255), -1)
        
        # Draw center line if available
        if center_x is not None:
            cv2.line(viz_frame, 
                    (int(center_x), roi_y_start), 
                    (int(center_x), roi_y_start + self.roi_height), 
                    (0, 255, 255), 2)
            
            # Draw a vertical line from the center to the bottom of the frame
            # This helps visualize where the robot is aiming
            cv2.line(viz_frame,
                    (int(center_x), roi_y_start + self.roi_height),
                    (int(center_x), height),
                    (0, 255, 255), 1, cv2.LINE_DASH)
        
        # Draw frame center
        frame_center = width // 2
        cv2.line(viz_frame, 
                (frame_center, roi_y_start), 
                (frame_center, roi_y_start + self.roi_height), 
                (255, 255, 255), 1)
        
        # Display offset and speed info
        left_speed, right_speed = self.control_robot()
        offset_text = f"Offset: {self.center_offset:.2f}"
        speed_text = f"Speed L/R: {left_speed:.1f}/{right_speed:.1f}"
        cv2.putText(viz_frame, offset_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(viz_frame, speed_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Create a binary visualization
        binary_colored = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        return viz_frame, binary_colored

    def run(self):
        """Main loop for the stripe follower"""
        try:
            while True:
                # Capture frame
                ret, frame = self.camera.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                # Process the frame
                roi, binary, edges = self.preprocess_frame(frame)
                left_center, right_center, valid_stripes = self.detect_stripes(binary, edges)
                
                # Calculate center position if both stripes are detected
                center_x = None
                if left_center is not None and right_center is not None:
                    center_x = self.calculate_center_position(left_center, right_center, frame.shape[1])
                    
                    # Control the robot
                    left_speed, right_speed = self.control_robot()
                    print(f"Left speed: {left_speed}, Right speed: {right_speed}")
                    
                    # Uncomment if using an actual robot
                    # self.robot.set_motor_speeds(left_speed, right_speed)
                else:
                    # No stripes or only one stripe detected
                    # Uncomment if using an actual robot
                    # self.robot.stop()
                    print("Stripes not detected properly")
                
                # Visualization for debugging
                if self.debug_mode:
                    viz_frame, binary_viz = self.visualize(frame, roi, binary, left_center, right_center, center_x, valid_stripes)
                    cv2.imshow("Stripe Follower", viz_frame)
                    cv2.imshow("Binary", binary_viz)
                    
                    # Exit on ESC key
                    if cv2.waitKey(1) == 27:
                        break
                        
                # Control the loop rate
                time.sleep(0.01)
                
        finally:
            # Clean up
            self.camera.release()
            cv2.destroyAllWindows()
            # Uncomment if using an actual robot
            # self.robot.stop()

if __name__ == "__main__":
    follower = StripeFollower()
    follower.run()