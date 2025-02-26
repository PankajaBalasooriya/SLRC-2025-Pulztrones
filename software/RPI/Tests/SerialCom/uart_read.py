import serial

# Open UART on /dev/serial0 (GPIO8 and GPIO10)
ser = serial.Serial("/dev/serial0", baudrate=115200, timeout=1)

print("Listening for UART data...")

try:
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")

except KeyboardInterrupt:
    print("Exiting...")
    ser.close()
