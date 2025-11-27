import serial, time
SERIAL_PORT = "COM10"   # <- change if needed
BAUD = 115200
ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
time.sleep(2)
for i in range(20):
    line = ser.readline().decode(errors='ignore').strip()
    print(i, line)
ser.close()
