import hypermedia.net.*;    // import UDP library
 
UDP udp;  // define the UDP object (sets up)
 
void setup() {
  size(480,640);
  background (255);
  smooth();
   
   udp = new UDP( this, 6000 );
    
 
}
 
 
 
void draw() {;}    //process events
 
 
 
   
 
void mousePressed (){
   String message  = str( key );    // the message to send
    String ip       = "127.0.1.1";   // the remote IP address of Host
    int port        = 8080;     // the destination port
     
    // formats the message for Pd
    message = pmouseX + "&" + pmouseY;
    // send the message
    udp.send( message, ip, port );
     ellipse(mouseX, mouseY, 5, 5);
     udp.listen();
}

void receive(byte[] data, String ip, int portRX){
  
String value=new String(data);
println(value);
}
