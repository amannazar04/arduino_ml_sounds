# collect_data.py
import serial
import json
import csv
import time
import sys
import os

# CONFIG - change SERIAL_PORT to your Arduino port
SERIAL_PORT = "COM10"   # <-- change this
BAUD = 115200
OUTPUT_CSV = "samples.csv"
LABELS = ["quiet", "noise"]   # only these two labels
SAMPLES_PER_LABEL = 30
READ_TIMEOUT = 5  # seconds per sample

def open_serial(port, baud):
    try:
        ser = serial.Serial(port, baud, timeout=0.5)
        time.sleep(2)
        return ser
    except Exception as e:
        print("Failed to open serial:", e)
        sys.exit(1)

def read_json_line(ser, timeout=READ_TIMEOUT):
    end = time.time() + timeout
    while time.time() < end:
        raw = ser.readline().decode(errors='ignore').strip()
        if not raw:
            continue
        if not raw.startswith("{"):
            # print("DEBUG (non-json):", raw)
            continue
        try:
            j = json.loads(raw)
            return j
        except:
            # print("Malformed json line:", raw)
            continue
    return None

def main():
    if not os.path.exists(OUTPUT_CSV):
        first_time = True
    else:
        first_time = False

    ser = open_serial(SERIAL_PORT, BAUD)
    out = open(OUTPUT_CSV, "a", newline='')
    writer = csv.writer(out)
    if first_time:
        writer.writerow(["rms","ptp","mean_abs","zcr","do_count","do","label"])
        out.flush()

    print("Starting data collection for labels:", LABELS)
    print("Samples per label:", SAMPLES_PER_LABEL)
    try:
        for lab in LABELS:
            input(f"\nPrepare '{lab}' samples and press ENTER to start collecting {SAMPLES_PER_LABEL} rows...")
            print(f"Collecting '{lab}'...")
            count = 0
            while count < SAMPLES_PER_LABEL:
                j = read_json_line(ser, timeout=READ_TIMEOUT)
                if j is None:
                    print("Timeout waiting for JSON. Ensure Arduino is running and Serial Monitor is closed.")
                    ans = input("Type 'r' to retry, 's' to skip this sample, 'a' to abort: ").strip().lower()
                    if ans == 'r' or ans == '':
                        continue
                    elif ans == 's':
                        writer.writerow([float('nan'), -1, float('nan'), float('nan'), -1, -1, lab])
                        out.flush()
                        count += 1
                        print(f"[{lab}] Skipped sample written as placeholder.")
                        continue
                    else:
                        raise KeyboardInterrupt
                # get features with fallback
                rms = float(j.get("rms", float('nan')))
                ptp = int(j.get("ptp", -1))
                mean_abs = float(j.get("mean_abs", float('nan')))
                zcr = float(j.get("zcr", float('nan')))
                do_count = int(j.get("do_count", j.get("do", 0)))
                do = int(j.get("do", 0))
                writer.writerow([rms, ptp, mean_abs, zcr, do_count, do, lab])
                out.flush()
                count += 1
                print(f"[{lab}] Saved {count}/{SAMPLES_PER_LABEL}: rms={rms:.6f}, ptp={ptp}, do_count={do_count}, do={do}")
            print(f"Finished collecting '{lab}'.")
    except KeyboardInterrupt:
        print("\nCollection aborted by user; saved partial data.")
    finally:
        out.close()
        ser.close()
        print("Done. CSV:", OUTPUT_CSV)

if __name__ == "__main__":
    main()
