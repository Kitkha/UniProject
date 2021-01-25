#include <RCSwitch.h>
RCSwitch mySwitch = RCSwitch();

void setup() {
  // Transmitter is connected to Arduino Pin #2
  mySwitch.enableTransmit(2);
}

void loop() {
  /* Using decimal code */
  mySwitch.send(100001, 24);
}
