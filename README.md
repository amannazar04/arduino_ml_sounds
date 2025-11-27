🌟 Arduino Sound Classifier (Quiet / Noise) — Offboard TinyML using Python + UNO + KY-037
<div align="center">
🔊 Real-time audio classification using

Arduino UNO + KY-037 + Python ML Server + High-Frequency Serial Bridge

A clean, fast, and educational TinyML-style project that runs advanced ML models offboard on a Python server while the Arduino performs feature extraction.

</div>
<div align="center">








</div>
🚀 Project Overview

This project is a real-time two-class sound classifier (quiet vs noise) built using:

Arduino UNO for capturing sound through the KY-037 microphone module

High-speed feature extraction on Arduino (RMS, peak-to-peak, zero-crossing rate, DO count)

Python-based ML model (RandomForest) trained on your own data

A local Flask server to classify incoming feature vectors

A high-frequency serial bridge sending JSON data between Arduino ↔ Python at ~50–100 classifications per second

This architecture allows you to run advanced ML models without needing an ESP32 or edge AI hardware — perfect for education, demos, or hobby projects.

🧠 Why This Project is Special

✔️ Uses window-based feature extraction (400 samples @ 5 kHz)

✔️ ML processed on Python → no memory limits on Arduino

✔️ Real-time performance (~20–60 classifications/sec)

✔️ Clean architecture with modular files

✔️ Super easy to extend: add new classes, new features, or swap ML models

✔️ Professional-level implementation suitable for GitHub, hackathons, or university projects


🔌 Hardware Setup
🛠️ Parts Required

Arduino UNO

KY-037 sound sensor module

Jumper wires

USB cable

Optional: LEDs for visual output

🔧 Wiring Diagram
KY-037      →     Arduino UNO
------------------------------
VCC         →     5V
GND         →     GND
OUT (Analog)→     A0
DO (Digital)→     D2


Make sure the KY-037 potentiometer is tuned so:

quiet → DO = 0

noise → DO = 1 (most of window)


🧩 How It Works (Step-by-Step)
1️⃣ Arduino captures 400 micro-samples @ 5 kHz

The Arduino computes:

RMS

Peak-to-peak (PTP)

Mean absolute amplitude

Zero-crossing rate (ZCR)

DO signal count

Last DO state

2️⃣ Arduino outputs JSON

Example:

{"rms":0.05,"ptp":112,"mean_abs":0.04,"zcr":0.12,"do":1,"do_count":312}

3️⃣ Python serial bridge reads these features

It forwards them to your ML server.

4️⃣ Flask ML server classifies sound

Example:

{ "label": "noise", "conf": 0.94 }

5️⃣ Arduino receives the label

It can light LEDs, trigger motors, or log data.

🧵 Setup Instructions


📥 1. Flash the Arduino

Upload:

uno_calibrate.ino


Ensure Serial Monitor is closed before running Python.

📦 2. Install Python dependencies

🎤 3. Collect Your Dataset

Run:

python collect_data.py


Follow prompts:

Collect 30× quiet

Collect 30× noise

This produces samples.csv.

🧠 4. Train your ML model
python train_model.py


This outputs:

Train accuracy: 1.00
Test accuracy: 0.95
Saved model to audio_model.joblib

💡 5. Start your ML server
python server.py


Runs on http://localhost:5000/classify.

🔗 6. Start real-time serial bridge
python serial_bridge.py


You will see:

→ quiet
→ noise
→ noise
→ quiet

✨ 7. Demo your classifier!

Clap, whistle, shake keys, rustle paper — watch classification change live.

Add LED code in Arduino to react visually.

🔍 Example Output
ptp=4 do_count=0 rms=0.004321
→ quiet

ptp=152 do_count=340 rms=0.123456
→ noise

