public class Snake
{
  private int id;
  private int nParts;
  private String[] direction;
  private float[] rotation;
  private float[] intensity;
  
  public Snake (int ID, int Nparts)
  {
    id = ID;
    nParts = Nparts;
    
    direction = new String[nParts];
    rotation = new float[nParts];
    intensity = new float[nParts];
  }
  
  public Snake (int ID)
  {
    id = ID;
    nParts = 3;
    
    direction = new String[nParts];
    rotation = new float[nParts];
    intensity = new float[nParts];
  }
  
  public void move(String[] dir, float[] rot, float[] inte){
      for(int i = 0;i<nParts;i++){        
        direction[i] = dir[i];
        rotation[i] = rot[i];
        intensity[i] = inte[i];
      }
  }
  
  public int getID(){
    return this.id;
  }
  
  public int getNparts(){
    return this.nParts;
  }
  
  public String[] getDirection(){
    return this.direction;
  }
  
  public float[] getRotation(){
    return this.rotation;
  }
  
  public float[] getIntensity(){
    return this.intensity;
  }
}