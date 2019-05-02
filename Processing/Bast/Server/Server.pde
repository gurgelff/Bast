import processing.net.*;
Server myServer;
int val = 0;

void setup() {
  size(200, 200);
  // Starts a myServer on port 10002
  myServer = new Server(this, 10002); 
}

void draw() {
  val = (val + 1) % 255;
  background(val);
  myServer.write(val);
}
