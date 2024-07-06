unsigned long previousMillis = 0;   // Variable to store the last time data was sent
const long interval = 1000;         // Interval between data transmissions (in milliseconds)

void setup() {
  Serial.begin(9600);               // Initialize serial communication at 9600 baud rate
  randomSeed(analogRead(0));        // Seed the random number generator with an analog pin reading
}

void loop() {
  unsigned long currentMillis = millis();  // Get the current time in milliseconds
  
  // Check if it's time to send data
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;  // Update the last sent time
    
    // Generate and send 9 random numbers between 5 and 50
    int data[9];
    for (int i = 0; i < 9; ++i) {
      data[i] = random(5, 51); // Generate random number between 5 and 50
    }
    
    // Send the data as CSV format
    Serial.print("[");
    for (int i = 0; i < 9; ++i) {
      Serial.print(data[i]);
      if (i < 8) {
        Serial.print(",");
      }
    }
    Serial.println("]");
  }
  
  // Check if there is incoming data on the serial port
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n'); // Read the incoming message until newline
    
    // Respond with "Received data: " followed by the received message
    Serial.print("Received data: ");
    Serial.println(msg);
  }
}
