# serial_bridge.py
import serial
import json
import requests
import time
import sys

SERIAL_PORT = "COM10"   # <-- CHANGE to your Arduino port (e.g., COM3 or /dev/ttyACM0)
BAUD = 115200
SERVER_URL = "http://localhost:5000/classify"

def open_serial(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=1)
        time.sleep(2)  # allow Arduino to reset
        return ser
    except Exception as e:
        print("Could not open serial port:", e)
        sys.exit(1)

def main():
    ser = open_serial(SERIAL_PORT, BAUD)
    print("Serial bridge started on", SERIAL_PORT)
    try:
        while True:
            raw = ser.readline().decode(errors='ignore').strip()
            if not raw:
                continue
            # ignore human-readable lines that don't start with {
            if not raw.startswith("{"):
                # optionally print debug
                # print("DEBUG:", raw)
                continue
            try:
                j = json.loads(raw)
            except Exception as e:
                print("Malformed JSON:", raw)
                continue
            try:
                resp = requests.post(SERVER_URL, json=j, timeout=2)
                data = resp.json()
                label = data.get("label", "unknown")
            except Exception as e:
                print("Server error:", e)
                label = "unknown"
            # send label back to Arduino
            ser.write((label + "\n").encode())
            print("Sent label ->", label)
    except KeyboardInterrupt:
        print("Exiting serial bridge.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
