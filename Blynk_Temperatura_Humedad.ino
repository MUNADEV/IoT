#define BLYNK_TEMPLATE_ID "TMPLGGm-SuC6" //Identificador del template en blynk
#define BLYNK_DEVICE_NAME "Alerta de temperatura" //Nombre de Device
#define BLYNK_AUTH_TOKEN "FWob55Ynwcr4ae1wSHOblRHgFk__yXlX" //Token
#define BLYNK_PRINT Serial

#define DHTPIN 2          // Pin donde está conectado el sensor
#define DHTTYPE DHT11     // De tipo DHT-11  

//Librerias
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <DHT.h>

char auth[] = BLYNK_AUTH_TOKEN;

//Credenciales de acceso a WIFI
char ssid[] = "NOMBRE"; //Nombre
char pass[] = "CONTRASEÑA";  //contrasena


DHT dht(DHTPIN, DHTTYPE);
BlynkTimer timer;

//Obtiene los datos
void obtenerDatos(){
  float h = dht.readHumidity(); //Humedad
  float t = dht.readTemperature(); // Temperatura
  if (isnan(h) || isnan(t)) {
    Serial.println("No es posible obtener datos del sensor");
    return;
  }

  Blynk.virtualWrite(V6, h);
  Blynk.virtualWrite(V5, t);
    Serial.print("Temperatura : ");
    Serial.print(t);
    Serial.print("    Humedad : ");
    Serial.println(h);

  // Si la temperatura es mayor a 10 grados
  if(t > 5){
    Blynk.email("r.millanao02@ufromail.cl", "Alerta, Alerta!..", " El helado se va a descongelar");
    Blynk.logEvent("alerta_temperatura","El helado se va a descongelar");
  }
  if(t < 1 && h >80){
    Blynk.email("r.millanao02@ufromail.cl", "Alerta, Alerta!..", " Los cultivos sufrirán daños por la humedad y el frío");
    Blynk.logEvent("alerta_temperatura","Los cultivos sufrirán daños por la humedad y el frío");
  }
  if(t > 30 && h < 5){
    Blynk.email("r.millanao02@ufromail.cl", "Alerta, Alerta!..", " Los cultivos necesitan riego");
    Blynk.logEvent("alerta_temperatura","Los cultivos necesitan riego");
  } 
}

void setup(){
  Serial.begin(115200);
  //Establecimiento de conexion
  Blynk.begin(auth, ssid, pass);
  //Iniciacion de dht
  dht.begin();
  timer.setInterval(2500L, obtenerDatos);
}

void loop(){
  Blynk.run();
  timer.run();
}