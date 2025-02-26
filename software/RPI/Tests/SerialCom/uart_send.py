import serial
import time

# Open UART on /dev/serial0 (uses GPIO 8 TX, GPIO 10 RX)
ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

count = 0  # Initialize counter

print("Sending data to STM32...")

try:
    while True:
        message = f"Count: {count}\n"
        ser.write(message.encode())  # Send data
        print(f"Sent: {message.strip()}")  
        
        count += 1  # Increment counter
        time.sleep(1)  # Send every second

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
