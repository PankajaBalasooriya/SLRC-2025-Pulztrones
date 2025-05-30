import time
import serial
from crc import Calculator, Crc16
import cv2
from pyzbar.pyzbar import decode
from pupil_apriltags import Detector
import numpy as np
import crcmod
import time


# Message IDs (must match STM32 firmware)
MSG_MOTOR_CMD = 0x01
MSG_SENSOR_DATA = 0x02
MSG_CV_RESULT = 0x03 
MSG_ACK = 0x7F

ser = serial.Serial(
    port='/dev/serial0',
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



def SerialMsgTest():
    i = 0
    while True:
        tag_data = str(i)
        msg = build_message(MSG_CV_RESULT, tag_data.encode('utf-8'))
        #ser.write(msg)
        print("msg", tag_data)
        i += 1
        time.sleep(0.1)
        
def SerialComTest():
    i = 0
    while True:
        tag_data = str(i)
        msg = build_message(MSG_CV_RESULT, tag_data.encode('utf-8'))
        ser.write(msg)
        print("msg", tag_data)
        i += 1
        time.sleep(0.1)
    

SerialComTest()
print("done")