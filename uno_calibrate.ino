// uno_calibrate.ino
// Windowed feature extractor for KY-037 (UNO)
// Produces JSON with: rms, ptp, mean_abs, zcr, do, do_count

#define MIC_A A0
#define DO_PIN 2

const int SAMPLE_COUNT = 400;     // window size
const int SAMPLE_DELAY_US = 200;  // ~5 kHz sampling
const int REPORT_DELAY_MS = 150;  // pause between windows

void setup(){
  Serial.begin(115200);
  pinMode(DO_PIN, INPUT);
  delay(2000);
}

void loop(){
  long sumSq = 0;
  long sumAbs = 0;
  int minv = 1023;
  int maxv = 0;
  int prevSign = 1;
  int zc = 0;
  int do_count = 0;
  int last_do = 0;

  for(int i=0;i<SAMPLE_COUNT;i++){
    int v = analogRead(MIC_A); // 0..1023
    int centered = v - 512;
    sumSq += (long)centered * centered;
    sumAbs += abs(centered);
    if (v < minv) minv = v;
    if (v > maxv) maxv = v;
    int sign = (centered >= 0) ? 1 : -1;
    if (i>0 && sign != prevSign) zc++;
    prevSign = sign;
    int d = digitalRead(DO_PIN);
    do_count += d;
    last_do = d;
    delayMicroseconds(SAMPLE_DELAY_US);
  }

  float rms = sqrt((double)sumSq / SAMPLE_COUNT) / 512.0;
  int ptp = maxv - minv;
  float mean_abs = (double)sumAbs / SAMPLE_COUNT / 512.0;
  float zcr = (float)zc / SAMPLE_COUNT;

  // human friendly
  Serial.print("ptp=");
  Serial.print(ptp);
  Serial.print(" do_count=");
  Serial.print(do_count);
  Serial.print(" rms=");
  Serial.print(rms,6);
  Serial.print("\n");

  // JSON for collector
  Serial.print("{\"rms\":");
  Serial.print(rms,6);
  Serial.print(",\"ptp\":");
  Serial.print(ptp);
  Serial.print(",\"mean_abs\":");
  Serial.print(mean_abs,6);
  Serial.print(",\"zcr\":");
  Serial.print(zcr,6);
  Serial.print(",\"do\":");
  Serial.print(last_do);
  Serial.print(",\"do_count\":");
  Serial.print(do_count);
  Serial.println("}");
  delay(REPORT_DELAY_MS);
}
