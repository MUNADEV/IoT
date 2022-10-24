import processing.serial.*;

Serial myPort;
String data="" ;
PFont myFont;

void setup(){
    size(1366,900); // tamanio de la ventana
    background(0);// color background negro
    myPort = new Serial(this, "COM3", 9600); //configuracion serial
    port
    myPort.b
    ufferUntil('\n');
}
void draw(){ //escribe la distancia
    background(0);
    textAlign(CENTER);
    fill(255);
    text(data,820,400);
    textSize(100);
    fill(#4B5DCE);
    text(" Distance : cm",450,400);
    noFill();
    stroke(#4B5DCE);
}
void serialEvent(Serial myPort){
    data=myPort.readStringUntil('\n');
}
