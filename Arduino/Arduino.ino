// HandCar
// (By) Xoán Carlos Cosmed Peralejo

// This is the software to the Arduino board.
// You have to complete the directional electric motors section, and review the main electric motor section.

int motorM1 = 5;
int motorM2 = 6;
int motorD1 = 12;
int motorD2 = 11;
int leds[] = {13};

char *cad;
char car;
int cont;


void setup() {

  Serial.begin(9600);

  pinMode(motorM1, OUTPUT);
  pinMode(motorM2, OUTPUT);
  pinMode(motorD1, OUTPUT);
  pinMode(motorD2, OUTPUT);
  for (int i = 0; i < sizeof(leds)/sizeof(leds[0]); i++)
    pinMode(leds[i], OUTPUT);

  cad = (char *)malloc(15*sizeof(char));
  cont = 0;

}

void loop() {

  while (Serial.available() > 0)
  {

    car = (char)Serial.read();
    Serial.println((char)car);

    if (car == '\n' || car == '\0' || car == ' ' || car == '*')
    {
      Serial.println("YYYYYY");
      cad[cont] = '\0';
      simularCoche(obtenerDatos(cad));
      cont = 0;
      cad = (char *)malloc(15*sizeof(char));
    }
    else
    {
      cad[cont] = (char)car;
      cont++;
    }

  }

}

int* obtenerDatos (char* cad) {

  int *datos = (int *)malloc(4*sizeof(int));

  datos[0] = (int)(cad[0]) - (int)('0');
  datos[3] = (int)(cad[2]-'0');
  datos[1] = (int)(cad[6]-'0');
  datos[2] = (int)(cad[8]-'0');

  // Temporary solution to the issue that takes the '0' received as -80
  for (int i = 0; i < 4; i++)
    if (datos[i]<0) datos[i] = 0;


  return datos;

}

void simularCoche(int *datos) {

 char cadena[15];
 sprintf(cadena, "%i-%i:::%i-%i", datos[0], datos[3], datos[1], datos[2]);
 Serial.println(cadena);

}

void moverCoche(int *datos) {

  /* Main motor */

  if (datos[0] > 0){

    analogWrite(motorM1, map(datos[0],0,9,0,254));
    analogWrite(motorM2, 0);

  } else if (datos[3] > 0){

    analogWrite(motorM1, 0);
    analogWrite(motorM2, map(datos[3],0,9,0,254));

  }

  /* Directional motor */

  // Here it goes the directional code. The information is safed in datos[1] and datos[2].

}

// (By) Xoan Carlos Cosmed Peralejo
