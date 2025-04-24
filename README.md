
# 🎮 Projeto Interativo com Arduino e Reconhecimento de Gestos

Este projeto é um jogo interativo que combina **Arduino**, **Python**, **MediaPipe** e **OpenCV** para criar uma experiência onde o jogador precisa resolver charadas com gestos para passar por um "portão mágico".

---

## 🧠 Conceito

O jogador é desafiado com charadas que exigem a execução de gestos específicos com as mãos. Se o gesto estiver correto, o Arduino responde com LEDs e som, simulando a liberação de um portão. O jogo integra visão computacional com feedback físico.

---

## 🛠️ Componentes Utilizados

### Hardware:
- 1 Arduino Uno
- 2 conjuntos de LEDs (vermelho, amarelo, verde)
- 1 Buzzer (ativo)
- 1 Servo motor 
- Protoboard e jumpers
- Cabo USB

### Software:
- Python 3
- OpenCV
- MediaPipe
- Biblioteca Serial (`pyserial`)
- Arduino IDE

---

## 🎵 Música do Cofre (Zelda)

Ao finalizar corretamente o desafio, o nosso objetivo seria tocar a música do baú de **The Legend of Zelda**, usando o buzzer do Arduino, porém após algumas dificuldades decidimos seguir com uma genérico.

---

## 🧩 Regras do Jogo

1. O sistema sorteia perguntas como:
   - "Qual o sinal do Bob Marley?"
   - "Sinal de quando você curte um vídeo?"
2. O jogador deve fazer o gesto correspondente.
3. Ao acertar, LEDs mudam, indicando o progresso do jogador.
4. Ao concluir com sucesso o desafio o buzzer emite o som da vitória.
5. O servo motor inicia seu movimento, simulando a abertura do portão mágico.

---

## 🎮 Comandos Arduino via Serial

- `'Y'`: Indica acerto na primeira etapa (libera LED verde).
- `'H'`: Avança na segunda etapa (amarelo ativo).
- `'G'`: Comando final — toca música e libera acesso.
  
---

## 💻 Código Python

O código Python usa a webcam para detectar a mão do jogador e reconhece os seguintes gestos:

| Gesto       | Configuração dos dedos |
|-------------|------------------------|
| `paz`     | ✌ (dedos 2 e 3 levantados) |
| `joinha` | 👍 (só polegar levantado) |
| `hangloose` | 🤙 (polegar e mindinho) |
| `five`      | ✋ (todos os dedos)     |

---

## 🖥️ Como Usar

1. Monte o circuito no Arduino com os LEDs e buzzer, de acordo com o código.
2. Faça o upload do código `.ino` usando o Arduino IDE.
3. Instale o Anaconda para gerenciar as dependências do Python, instalando os pacotes necessários

   ```bash
   pip install opencv-python mediapipe pyserial
   ```

4. Responda as perguntas fazendo os gestos certos para liberar o portão!


## 🚀 Futuras Implementações

- Estrutura real de um portão medieval.
- Mais perguntas e reconhecimento de outros gestos.
- Integração com pontuação e fases do jogo.

---

Desenvolvido por:
Rodrigo Brasileiro RM:98952
Nikolas Rodrigues Moura dos Santos RM:551566
