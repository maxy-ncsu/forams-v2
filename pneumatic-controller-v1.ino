// Arduino code for rp2040 in pneumatics system

// Pins used on raspi pico for control
int SOLENOID_1 = 16;
int SOLENOID_2 = 17;
int SOLENOID_3 = 18;
int SOLENOID_4 = 19;
int SOLENOID_5 = 20;
int SOLENOID_6 = 21;

// variable data received from serial is stored
int data;
// array of pins being high or low
int sol_arr[7] = {0, 0, 0, 0, 0, 0, 0};

void setup() {
  // 9600 baud rate
  Serial.begin(9600);
  // Pins set to output
  pinMode(SOLENOID_1, OUTPUT);
  pinMode(SOLENOID_2, OUTPUT);
  pinMode(SOLENOID_3, OUTPUT);
  pinMode(SOLENOID_4, OUTPUT);
  pinMode(SOLENOID_5, OUTPUT);
  pinMode(SOLENOID_6, OUTPUT);
  // Pins default to low, valve closed
  digitalWrite(SOLENOID_1, LOW);
  digitalWrite(SOLENOID_2, LOW);
  digitalWrite(SOLENOID_3, LOW);
  digitalWrite(SOLENOID_4, LOW);
  digitalWrite(SOLENOID_5, LOW);
  digitalWrite(SOLENOID_6, LOW);
}

void loop() {
  // read data from COM micro usb interface
  data = Serial.read();

  // open or close valve based on signal
  // 1-6 switches valve to opposite state
  switch (data) {
    case '1':
      if (sol_arr[1]) {
        digitalWrite(SOLENOID_1, LOW);
      }
      else {
        digitalWrite(SOLENOID_1, HIGH);
      }

      sol_arr[1] = !sol_arr[1];
      break;
    case '2':
      if (sol_arr[2]) {
        digitalWrite(SOLENOID_2, LOW);
      }
      else {
        digitalWrite(SOLENOID_2, HIGH);
      }

      sol_arr[2] = !sol_arr[2];
      break;
    case '3':
      if (sol_arr[3]) {
        digitalWrite(SOLENOID_3, LOW);
      }
      else {
        digitalWrite(SOLENOID_3, HIGH);
      }

      sol_arr[3] = !sol_arr[3];
      break;
    case '4':
      if (sol_arr[4]) {
        digitalWrite(SOLENOID_4, LOW);
      }
      else {
        digitalWrite(SOLENOID_4, HIGH);
      }

      sol_arr[4] = !sol_arr[4];
      break;
    case '5':
      if (sol_arr[5]) {
        digitalWrite(SOLENOID_5, LOW);
      }
      else {
        digitalWrite(SOLENOID_5, HIGH);
      }

      sol_arr[5] = !sol_arr[5];
      break;
    case '6':
      if (sol_arr[6]) {
        digitalWrite(SOLENOID_6, LOW);
      }
      else {
        digitalWrite(SOLENOID_6, HIGH);
      }

      sol_arr[6] = !sol_arr[6];
      break;

    // 0 closes all the valves
    case '0':
      digitalWrite(SOLENOID_1, LOW);
      digitalWrite(SOLENOID_2, LOW);
      digitalWrite(SOLENOID_3, LOW);
      digitalWrite(SOLENOID_4, LOW);
      digitalWrite(SOLENOID_5, LOW);
      digitalWrite(SOLENOID_6, LOW);
      break;
  }
}
