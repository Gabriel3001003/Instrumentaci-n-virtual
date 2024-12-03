#include <SPI.h>
#include <MFRC522.h>

// Pines del RFID-RC522
#define SS_PIN 10
#define RST_PIN 9

MFRC522 rfid(SS_PIN, RST_PIN); // Crear objeto MFRC522

// Pines de los LEDs
#define LED_AMARILLO 6
#define LED_VERDE 5
#define LED_ROJO 4

void setup() {
  // Configurar comunicación serial
  Serial.begin(9600); // Comunicación con Python (puerto serial)
  SPI.begin();        // Iniciar SPI
  rfid.PCD_Init();    // Iniciar módulo RFID

  // Configurar los pines de los LEDs como salida
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO, OUTPUT);

  // Encender el LED amarillo indicando que está esperando lectura
  digitalWrite(LED_AMARILLO, HIGH);
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_ROJO, LOW);
}

void loop() {
  // Revisar si hay una nueva tarjeta
  if (!rfid.PICC_IsNewCardPresent()) {
    return;  // Si no hay tarjeta, seguimos esperando
  }

  // Revisar si podemos leer la tarjeta
  if (!rfid.PICC_ReadCardSerial()) {
    errorLectura();  // Si no podemos leer, indicamos error
    return;
  }

  // Apagar el LED amarillo porque ya se detectó una tarjeta
  digitalWrite(LED_AMARILLO, LOW);

  // Leer el UID de la tarjeta y enviarlo por Serial a Python
  String uid = "";
  for (byte i = 0; i < rfid.uid.size; i++) {
    uid += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");  // Formato para agregar ceros
    uid += String(rfid.uid.uidByte[i], HEX);
  }

  uid.toUpperCase();  // Convertir a mayúsculas el UID
  Serial.println(uid);  // Enviar UID al puerto serial para Python

  // Encender el LED verde indicando que la lectura fue correcta
  digitalWrite(LED_VERDE, HIGH);
  delay(1000);  // Mantener el LED verde encendido por un segundo

  // Apagar el LED verde y volver a encender el LED amarillo para esperar otra lectura
  digitalWrite(LED_VERDE, LOW);
  digitalWrite(LED_AMARILLO, HIGH);

  // Parar la comunicación con la tarjeta actual
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}

void errorLectura() {
  // Encender el LED rojo indicando un error en la lectura
  digitalWrite(LED_ROJO, HIGH);
  delay(1000);  // Mantener el LED rojo encendido por un segundo

  // Apagar el LED rojo y volver a encender el LED amarillo para esperar otra lectura
  digitalWrite(LED_ROJO, LOW);
  digitalWrite(LED_AMARILLO, HIGH);
}
