#!/usr/bin/env python3
"""
Raspberry Pi UART Communication for Robot Control
This script handles computer vision tasks and communicates with STM32 via UART
"""

import serial
import time
import threading
import cv2
import numpy as np

# Communication protocol definitions
START_MARKER = b'<'
END_MARKER = b'>'

# Command IDs
CMD_LINE_DETECTED = 0x01
CMD_GRID_POSITION = 0x02
CMD_COLOR_DETECTED = 0x03
CMD_START_LINE_FOLLOWING = 0x11
CMD_START_GRID_NAVIGATION = 0x12
CMD_START_TASK_1_COLOR_DETECTION = 0x13
CMD_STOP = 0x20

class RobotComm:
    def __init__(self, serial_port='/dev/serial0', baud_rate=115200):
        """Initialize UART communication with STM32"""
        self.serial = serial.Serial(
            port=serial_port,
            baudrate=baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        
        # Initialize state variables
        self.rx_state = 'WAITING_FOR_START'
        self.rx_buffer = bytearray()
        self.rx_cmd = 0
        self.rx_length = 0
        
        # Initialize operation mode
        self.current_mode = None
        
        # Initialize camera
        self.camera = cv2.VideoCapture(0)  # Use camera index 0
        if not self.camera.isOpened():
            print("Error: Could not open camera")
        
        # Set camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Flag to control processing threads
        self.running = True
        
        # Start receive thread
        self.rx_thread = threading.Thread(target=self.receive_data)
        self.rx_thread.daemon = True
        self.rx_thread.start()
        
        # Vision processing thread
        self.vision_thread = None
        
        print("Robot communication initialized")
    
    def __del__(self):
        """Clean up resources on object destruction"""
        self.running = False
        if self.serial.is_open:
            self.serial.close()
        if self.camera.isOpened():
            self.camera.release()
    
    def receive_data(self):
        """Thread function to receive and process data from STM32"""
        while self.running:
            if self.serial.in_waiting > 0:
                # Read one byte
                rx_byte = self.serial.read(1)
                
                # State machine for packet reception
                if self.rx_state == 'WAITING_FOR_START':
                    if rx_byte == START_MARKER:
                        self.rx_state = 'WAITING_FOR_CMD'
                
                elif self.rx_state == 'WAITING_FOR_CMD':
                    self.rx_cmd = int.from_bytes(rx_byte, byteorder='little')
                    self.rx_state = 'WAITING_FOR_LENGTH'
                
                elif self.rx_state == 'WAITING_FOR_LENGTH':
                    self.rx_length = int.from_bytes(rx_byte, byteorder='little')
                    self.rx_buffer = bytearray()
                    if self.rx_length > 0:
                        self.rx_state = 'RECEIVING_DATA'
                    else:
                        self.rx_state = 'WAITING_FOR_END'
                
                elif self.rx_state == 'RECEIVING_DATA':
                    self.rx_buffer.extend(rx_byte)
                    if len(self.rx_buffer) >= self.rx_length:
                        self.rx_state = 'WAITING_FOR_END'
                
                elif self.rx_state == 'WAITING_FOR_END':
                    if rx_byte == END_MARKER:
                        # Process complete packet
                        self.process_command()
                    # Reset state machine for next packet
                    self.rx_state = 'WAITING_FOR_START'
            
            # Sleep briefly to reduce CPU usage
            time.sleep(0.001)
    
    def process_command(self):
        """Process received command from STM32"""
        print(f"Received command: {self.rx_cmd}")
        
        if self.rx_cmd == CMD_START_LINE_FOLLOWING:
            # Stop any existing vision processing
            self.stop_vision_processing()
            # Start line following mode
            self.current_mode = 'line_following'
            self.vision_thread = threading.Thread(target=self.line_following_task)
            self.vision_thread.daemon = True
            self.vision_thread.start()
            
        elif self.rx_cmd == CMD_START_GRID_NAVIGATION:
            # Stop any existing vision processing
            self.stop_vision_processing()
            # Extract target coordinates
            if len(self.rx_buffer) >= 2:
                target_x = self.rx_buffer[0]
                target_y = self.rx_buffer[1]
                # Start grid navigation mode
                self.current_mode = 'grid_navigation'
                self.vision_thread = threading.Thread(target=self.grid_navigation_task, 
                                                    args=(target_x, target_y))
                self.vision_thread.daemon = True
                self.vision_thread.start()
            
        elif self.rx_cmd == CMD_START_COLOR_DETECTION:
            # Stop any existing vision processing
            self.stop_vision_processing()
            # Start color detection mode
            self.current_mode = 'color_detection'
            self.vision_thread = threading.Thread(target=self.color_detection_task)
            self.vision_thread.daemon = True
            self.vision_thread.start()
            
        elif self.rx_cmd == CMD_STOP:
            # Stop all processing
            self.stop_vision_processing()
    
    def stop_vision_processing(self):
        """Stop the current vision processing task"""
        if self.vision_thread and self.vision_thread.is_alive():
            self.current_mode = None
            # The thread will stop on next loop
            time.sleep(0.1)  # Give thread time to finish
    
    def send_command(self, cmd, data=None):
        """Send command to STM32"""
        # Create packet structure
        packet = bytearray()
        packet.extend(START_MARKER)
        packet.extend(cmd.to_bytes(1, byteorder='little'))
        
        if data is None:
            data = bytearray()
        
        packet.extend(len(data).to_bytes(1, byteorder='little'))
        packet.extend(data)
        packet.extend(END_MARKER)
        
        # Send packet
        self.serial.write(packet)
    
    def line_following_task(self):
        """Computer vision task for line following"""
        print("Starting line following task")
        
        while self.running and self.current_mode == 'line_following':
            # Capture frame
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Could not read from camera")
                time.sleep(0.1)
                continue
            
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to isolate the line (assuming black line on white background)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            
            # Process bottom half of image where line is expected
            height, width = thresh.shape
            roi = thresh[height//2:height, :]
            
            # Find contours
            contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Find the largest contour (the line)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Get the center of the contour
                M = cv2.moments(largest_contour)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    
                    # Calculate line position relative to center
                    # Positive value means line is to the right
                    line_position = cx - (width // 2)
                    line_position = 69 # Dummy
                    
                    # Calculate line angle (simplified)
                    # In a real implementation, you would use more points to calculate the angle
                    line_angle = 0  # Simplified
                    
                    # Scale line position to fit in a signed byte (-127 to 127)
                    normalized_position = max(min(line_position, 127), -127)
                    
                    # Send line detection data to STM32
                    data = bytearray([normalized_position & 0xFF, line_angle & 0xFF])
                    self.send_command(CMD_LINE_DETECTED, data)
            
            # Process at 30fps max
            time.sleep(0.033)
    
    def grid_navigation_task(self, target_x, target_y):
        """Computer vision task for grid navigation"""
        print(f"Starting grid navigation task to target ({target_x}, {target_y})")
        
        # For simplicity, we'll simulate grid detection
        # In a real implementation, you would detect a grid pattern using computer vision
        
        # Simulated robot position
        current_x, current_y = 0, 0
        orientation = 0  # 0=N, 1=E, 2=S, 3=W
        
        while self.running and self.current_mode == 'grid_navigation':
            # Capture frame
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Could not read from camera")
                time.sleep(0.1)
                continue
            
            # In a real implementation, you would:
            # 1. Detect grid lines
            # 2. Identify intersections
            # 3. Determine current position on grid
            
            # For this example, we'll just simulate position updates
            if current_x < target_x:
                current_x += 1
            elif current_x > target_x:
                current_x -= 1
                
            if current_y < target_y:
                current_y += 1
            elif current_y > target_y:
                current_y -= 1
            
            # Send grid position to STM32
            data = bytearray([current_x & 0xFF, current_y & 0xFF, orientation & 0xFF])
            self.send_command(CMD_GRID_POSITION, data)
            
            # Check if target reached
            if current_x == target_x and current_y == target_y:
                print("Target position reached")
                self.stop_vision_processing()
                break
            
            # Update at 2Hz for simulation
            # In real implementation, update based on frame rate
            time.sleep(0.5)
    
    def color_detection_task(self):
        """Computer vision task for color detection"""
        print("Starting color detection task")
        
        # Define color ranges in HSV
        color_ranges = {
            'red': ([0, 100, 100], [10, 255, 255]),  # Red color range
            'green': ([40, 100, 100], [80, 255, 255]),  # Green color range
            'blue': ([100, 100, 100], [140, 255, 255])  # Blue color range
        }
        
        color_ids = {'red': 1, 'green': 2, 'blue': 3}
        
        while self.running and self.current_mode == 'color_detection':
            # Capture frame
            ret, frame = self.camera.read()
            if not ret:
                print("Error: Could not read from camera")
                time.sleep(0.1)
                continue
            
            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            detected_color = None
            max_area = 0
            
            # Check for each color
            for color_name, (lower, upper) in color_ranges.items():
                # Create a mask for the color
                lower_bound = np.array(lower)
                upper_bound = np.array(upper)
                mask = cv2.inRange(hsv, lower_bound, upper_bound)
                
                # Find contours
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Find the largest contour
                if contours:
                    largest_contour = max(contours, key=cv2.contourArea)
                    area = cv2.contourArea(largest_contour)
                    
                    # If this color has the largest area so far, save it
                    if area > max_area and area > 1000:  # Minimum area threshold
                        max_area = area
                        detected_color = color_name
            
            # Send detected color to STM32
            if detected_color:
                color_id = color_ids[detected_color]
                print(f"Detected color: {detected_color} (ID: {color_id})")
                data = bytearray([color_id & 0xFF])
                self.send_command(CMD_COLOR_DETECTED, data)
            
            # Process at 10fps
            time.sleep(0.1)


if __name__ == "__main__":
    # Create robot communication object
    robot = RobotComm()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user")
    finally:
        # Clean up
        robot.running = False
        time.sleep(0.5)  # Give threads time to exit