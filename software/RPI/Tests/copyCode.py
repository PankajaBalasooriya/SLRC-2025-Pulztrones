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




def SerialComTest():
    i = 0
    while True:
        tag_data = str(i)
        msg = build_message(MSG_CV_RESULT, tag_data.encode('utf-8'))
        #ser.write(msg)
        print("msg", tag_data)
        i += 1
        
    
    

SerialComTest()
print("done")