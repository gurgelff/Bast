JSONObject json;
Snake[] snake = new Snake[10];

String[] dir = new String[3];
float[] inte = new float[3];
float[] rot = new float[3];

void setup() 
  {
    json = new JSONObject();
    snake[0] = new Snake(1);
    
  }

void draw()
{
  for(int x=0;x<3;x++){
    if (random(100)%2==0)
      dir[x] = "up";
    else
      dir[x] = "down";
      
    rot[x]=random(-30,30);
    inte[x]=random(100)/50;
  }
  
  delay(500);
  snake[0].move( dir,rot,inte );


    
  try
  {
        json.setString("direction1", snake[0].getDirection()[0]);
        json.setString("direction2", snake[0].getDirection()[1]);
        json.setString("direction3", snake[0].getDirection()[2]);
        json.setFloat("intensity1", snake[0].getIntensity()[0]);
        json.setFloat("intensity2", snake[0].getIntensity()[1]);
        json.setFloat("intensity3", snake[0].getIntensity()[2]);
        json.setFloat("rotation", snake[0].getRotation()[0]);
        saveJSONObject(json, "/home/fernando/Projetos/Python/Bast/cmd.json");
   }
   catch (Exception e) 
   {
    e.printStackTrace();
  }
}