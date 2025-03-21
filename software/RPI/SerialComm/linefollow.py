import cv2
import time

class LineDetector:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)  # Open default camera

    def process_frame(self):
        while True:
            # Capture frame
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Could not read from camera")
                time.sleep(0.1)
                continue
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to isolate the line
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            
            # Process bottom half of image where line is expected
            height, width = thresh.shape
            roi = thresh[height//2:height, :]
            
            # Find contours
            contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get the center of the contour
                M = cv2.moments(largest_contour)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"]) + height // 2  # Adjust to full frame
                    
                    # Calculate line position relative to center
                    line_position = cx - (width // 2)
                    
                    # Draw contours
                    cv2.drawContours(frame[height//2:height, :], [largest_contour], -1, (0, 255, 0), 2)
                    
                    # Draw center point of detected line
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    
                    # Display line position info
                    cv2.putText(frame, f"Line Position: {line_position}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
            # Show frames
            cv2.imshow("Line Detection", frame)
            cv2.imshow("Thresholded Image", thresh)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = LineDetector()
    detector.process_frame()
