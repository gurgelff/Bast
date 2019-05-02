//import ui library for buttons
import controlP5.*;
ControlP5 cp5;

//import udp library
import hypermedia.net.*;
UDP udpRX,udpTX;

//variables for udp
String ip="localhost";
int portRX=8080;
int portTX=8081;
int rx_buffer_size=100;
String rx_string="Waiting for Data";
byte[] rx_byte=new byte[rx_buffer_size];
int rx_byte_count=0;

//set strings for sending on udp
String s0="Zero";
String s1="One";
String s2="Two";

void setup(){

  //set window dimensions
  size(700,300);
  
  //disables drawing outlines
  noStroke();
  
  //create new cp5 object for this user
  cp5=new ControlP5(this);
  
  //create 3 buttons 
  for (int i=0;i<3;i++){
    cp5.addBang("Send"+i)
       .setPosition(400+i*80,200)
       .setSize(60,40)
       .setColorForeground(140)
       .setId(i)
       ; 
  }//end of for loop 

  //create new object for transmitting
  udpTX=new UDP(this,portTX,ip);
  udpTX.log(true);
  udpTX.setBuffer(5);
  udpTX.loopback(true);
  
  //create new object for receiving 
  udpRX=new UDP(this,portRX,ip);
  udpRX.log(true);
  udpRX.listen(true);

  
  //confirm if tx is multicast and loopback is disabled
  println("Is TX mulitcast: "+udpTX.isMulticast());
  println("Has TX joined multicast: "+udpTX.isJoined());
  println("Is loopback enabled on TX: "+udpTX.isLoopback());
  
  //confirm if rx is multicast 
  println("Is RX mulitcast: "+udpRX.isMulticast());
  println("Has RX joined multicast: "+udpRX.isJoined());



//stop looping setup  
noLoop();

}//end of setup()


void draw(){
  
  //set background color, also clears the screen
  background(0);
  
  
  //misc
  int off_x=200;
  
  //main title 
  fill(255);
  textSize(25);
  text("UDP Tool",20,30);
  
  fill(200);
  
  //IP address
  textSize(20);
  text("IP Address:",20,30+25);
  fill(252,10,55);
  text(ip,130,30+25);
  
  fill(200);
  
  //UDP ports
  text("Port(Sending):",20,30+25+20);
  fill(252,10,55);
  text(portRX,155,30+25+20);
  
  fill(200);
  
  text("Port(Receiving):",20,30+25+40);
  fill(252,10,55);
  text(portTX,170,30+25+40);
  
  fill(200);
  
  text("Last Packet Received:",20,30+25+120);
  fill(252,10,55);
  text(rx_string,230,30+25+120);
  
  fill(200);
  text("Total Bytes Recieved:",20,30+25+140);
  fill(252,10,55);
  text(rx_byte_count,230,30+25+140);
  //start looping draw
  loop();
  
}//end of draw()


//event handling 
public void controlEvent(ControlEvent theEvent) {

    if(theEvent.getController().getId()==0){
    println("String Sent: "+s0);
    udpTX.send(s0,ip,portTX);
    }
    
    if(theEvent.getController().getId()==1){
    println("String Sent: "+s1);
    udpTX.send(s1,ip,portTX);
    }
    
    if(theEvent.getController().getId()==2){
    println("String Sent: "+s2);
    udpTX.send(s2,ip,portTX);
    }
   
    
}//end of event


//udp receive handling
void receive(byte[] data, String ip, int portRX){
  
String value=new String(data);
println(value);
rx_byte_count+=data.length;

//clear receive byte array
for(int j=0;j<rx_byte.length;j++)
{
  rx_byte[j]=0;
}

//copy received bytes to rx_byte array
arrayCopy(data,rx_byte);

//copy bytes to a string and trim string to remove nulls
rx_string=new String(rx_byte);
rx_string=trim(rx_string);

//is called to update the received string
redraw();
}
