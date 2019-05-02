  

// Example by Tom Igoe 
// Creates a client that sends input to a server

import processing.net.*; 
Client myClient; 
int clicks;
int dataIn;

void setup() { 
  // Connect to the local machine at port 10002.
  // This example will not run if you haven't
  // previously started a server on this port.
  size(200,200);
  myClient = new Client(this, "127.0.0.1", 8080);
  myClient.write("\n\n Lambda1\n\n");
  

} 

void draw() { 
  // Change the background if the mouse is pressed
  
  if (mousePressed) {
    background(255);
  } 
  else
  {
    background(0);
  }
  

  
  if (keyPressed)
  {
    if (key == '1')
      myClient.write("1");
    if (key == 'q')
      myClient.write("end");  
    if (key == 'w')
      myClient.write("{type: cylinder, axis: 3, posX: 25.7}");  
      
      
  }
} 

void clientEvent(Client someClient) {
  //print("\nServer Says:  ");
  String str = myClient.readString();
  print(str);
}


