#include <Arduino_LSM6DS3.h>

int H[] = { 4, 0, 0, 0, 0 },
    E[] = { 1, 0 },
    L[] = { 4, 0, 1, 0, 0 },
    O[] = { 3, 1, 1, 1 },
    I[] = { 2, 0, 0 },
    M[] = { 2, 1, 1 },
    U[] = { 3, 0, 0, 1 },
    SPACE[] = { 10 };
int sht = 500, lng = 1000;
bool verbose = false;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");

    while (1);
  }

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  int* str[] = {
    H, E, L, L, O,
    I, M, U
  };

  for (int letter = 0; letter < sizeof(str) / sizeof(str[0]); letter++) {
    displayIMU();
    
    for (int on = 1; on < str[letter][0] + 1; on++) {
      displayIMU();
      digitalWrite(LED_BUILTIN, HIGH);
      if (str[letter][on]) {
        if (verbose) Serial.print("-");
        delay(lng);
      }
      else {
        if (verbose) Serial.print(".");
        delay(sht);
      }

      digitalWrite(LED_BUILTIN, LOW);
      displayIMU();
      delay(sht);
      displayIMU();
    }
    if (verbose) Serial.println("/");
    displayIMU();
    delay(lng);
    displayIMU();
  }
}

void displayIMU() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.println("Acceleration in g's");
    Serial.print("ax = ");
    Serial.println(x);
    Serial.print("ay = ");
    Serial.println(y);
    Serial.print("az = ");
    Serial.println(z);
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    Serial.println("Gyroscope in degrees/second");
    Serial.print("gx = ");
    Serial.println(x);
    Serial.print("gy = ");
    Serial.println(y);
    Serial.print("gz = ");
    Serial.println(z);
  }
}
