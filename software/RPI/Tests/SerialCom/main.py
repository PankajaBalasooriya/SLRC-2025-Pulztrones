import time
import serial
from crc import Calculator, Crc16
import cv2
from pyzbar.pyzbar import decode
from pupil_apriltags import Detector
import numpy as np

import crcmod

def calc_crc(data):
    crc16_func = crcmod.predefined.mkCrcFun('crc-16')
    crc_value = crc16_func(data)
    return crc_value.to_bytes(2, 'big')  # Convert to 2-byte big-endian format

# Message IDs (must match STM32 firmware)
MSG_MOTOR_CMD = 0x01
MSG_SENSOR_DATA = 0x02
MSG_CV_RESULT = 0x03  # Add this line
MSG_ACK = 0x7F

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1    
)




def build_message(msg_id, data):
    stx = b'\x02'
    etx = b'\x03'
    payload = bytes([msg_id, len(data)]) + data
    crc = calc_crc(payload)
    return stx + payload + crc + etx

def parse_message(buffer):
    if buffer.startswith(b'\x02') and b'\x03' in buffer:
        etx_pos = buffer.find(b'\x03')
        packet = buffer[1:etx_pos-2]
        crc_received = buffer[etx_pos-2:etx_pos]
        if calc_crc(packet) == crc_received:
            return packet[0], packet[2:2+packet[1]]
    return None, None

# def cv_processing():
#     cap = cv2.VideoCapture(0)
#     while True:
#         ret, frame = cap.read()
#         # AprilTag detection
#         results = decode(frame)
#         if results:
#             msg = build_message(MSG_CV_RESULT, results[0].data)
#             ser.write(msg)
#             print(results)

def cv_processing():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    at_detector = Detector(families='tag25h9')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        tags = at_detector.detect(gray, estimate_tag_pose=False)
        
        for tag in tags:
            print("Det 1")
            corners = tag.corners.astype(int)
            for i in range(4):
                cv2.line(frame, tuple(corners[i]), tuple(corners[(i+1) % 4]), (0, 255, 0), 2)
            
            center_x, center_y = int(tag.center[0]), int(tag.center[1])
            tag_data = str(tag.tag_id)
            cv2.putText(frame, tag_data, (center_x, center_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            msg = build_message(MSG_CV_RESULT, tag_data.encode('utf-8'))
            ser.write(msg)
            print("Detected Tag:", tag_data)
        
        # Display the camera feed with detected tags
        cv2.imshow("AprilTag Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

cv_processing()
print("done")