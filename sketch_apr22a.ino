#include <Servo.h>  // biblioteca do servo

Servo portao;

// Define os LEDs
#define ledG1 5
#define ledY1 6
#define ledR1 7
#define ledG2 8
#define ledY2 9
#define ledR2 10

// Notas para a música 
#define NOTE_G3 196
#define NOTE_A3 220
#define NOTE_C4 262
#define NOTE_B3 247

// Define o Buzzer
#define BUZZER_PIN 4

// Define o Servo
#define SERVO_PIN 3  

//Define a sequência da músia
int melody[] = {
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};

// duração das notas: 4 = um quarto, 8 = um oitavo, etc.
int noteDurations[] = {
  4, 8, 8, 4, 4, 4, 4, 4
};

// Função para tocar a música
void tocarZeldaBau() {
  for (int thisNote = 0; thisNote < 8; thisNote++) {
    int noteDuration = 1000 / noteDurations[thisNote];
    tone(BUZZER_PIN, melody[thisNote], noteDuration);
    int pauseBetweenNotes = noteDuration * 1.30;
    delay(pauseBetweenNotes);
    noTone(BUZZER_PIN);
  }
}

void setup() {
  Serial.begin(9600);
  
  // Configura pinos dos LEDs
  pinMode(ledR1, OUTPUT);
  pinMode(ledR2, OUTPUT);
  pinMode(ledY1, OUTPUT);
  pinMode(ledY2, OUTPUT);
  pinMode(ledG1, OUTPUT);
  pinMode(ledG2, OUTPUT);

  // Configura buzzer
  pinMode(BUZZER_PIN, OUTPUT);

  // Estado inicial dos LEDs
  digitalWrite(ledR1, HIGH);
  digitalWrite(ledR2, HIGH);
  digitalWrite(ledY1, LOW);
  digitalWrite(ledY2, LOW);
  digitalWrite(ledG1, LOW);
  digitalWrite(ledG2, LOW);

  // Conecta o servo e posiciona em 0°
  portao.attach(SERVO_PIN);
  portao.write(0);

}

void loop() {
  if (Serial.available() > 0) {
    char comando = Serial.read();

    if (comando == 'Y') { // Y de yellow que indica que a primeira etapa foi concluída
      digitalWrite(ledR1, LOW);
      digitalWrite(ledR2, LOW);
      digitalWrite(ledY1, LOW);
      digitalWrite(ledY2, HIGH);
      digitalWrite(ledG1, HIGH);
      digitalWrite(ledG2, LOW);
      delay(5000);
      digitalWrite(ledR1, HIGH);
      digitalWrite(ledY2, HIGH);
      digitalWrite(ledG1, LOW);
    }

    else if (comando == 'G') { // G de green que significa que a segunda etapa foi concluída
      digitalWrite(ledR1, LOW);
      digitalWrite(ledR2, LOW);
      digitalWrite(ledY1, LOW);
      digitalWrite(ledY2, LOW);
      digitalWrite(ledG2, HIGH);
      digitalWrite(ledG1, HIGH);
      tocarZeldaBau();  
      portao.write(180);  // abre o portão
    }

    else if (comando == 'H') { //H de Half que significa que metade da segunda etapa foi concluída
      digitalWrite(ledR1, LOW);
      digitalWrite(ledR2, LOW);
      digitalWrite(ledY1, HIGH);
      digitalWrite(ledY2, LOW);
      digitalWrite(ledG1, LOW);
      digitalWrite(ledG2, LOW);
    }
  }
}
