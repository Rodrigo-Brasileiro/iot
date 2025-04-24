import cv2              # Biblioteca para capturar e exibir vídeo e imagens
import mediapipe as mp  # Biblioteca do Google para reconhecimento de gestos e poses
import serial           # Comunicação com o Arduino via porta serial
import time             # Usado para temporizações no código (ex: delay)
import random           # Utilizado para sortear perguntas aleatórias

# Inicia comunicação com o Arduino (ajuste 'COM7' se necessário)
arduino = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)  # Aguarda o Arduino inicializar

# Inicializa o módulo de reconhecimento de mãos do MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils  # Utilizado para desenhar as conexões das mãos na tela

# Função para interpretar os gestos com base nos dedos levantados
def reconhecer_gesto(hand_landmarks):
    dedos = []
    tips = [4, 8, 12, 16, 20]  # Índices dos dedos na estrutura do MediaPipe

    # Verifica se o dedão está levantado (compara posição horizontal)
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        dedos.append(1)
    else:
        dedos.append(0)

    # Verifica os outros dedos (compara posição vertical)
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y:
            dedos.append(1)
        else:
            dedos.append(0)

    # Interpretação de gestos com base nos dedos levantados
    if dedos == [0, 1, 1, 0, 0]:
        return "paz"
    elif dedos == [0, 0, 0, 0, 1]:
        return "joinha"
    elif dedos == [0, 1, 0, 0, 1]:
        return "hangloose"
    elif dedos == [1, 1, 1, 1, 1]:
        return "five"
    else:
        return "desconhecido"

# Dicionário com perguntas e gestos correspondentes esperados
perguntas_gestos = {
    "Sinal do Bob Marley": "paz",
    "Quando voce curte um video": "joinha",
    "Sinal do Ronaldinho": "hangloose",
    "HIGH FIVE": "five"
}

# Gera uma nova sequência aleatória de 2 perguntas
def nova_sequencia():
    return random.sample(list(perguntas_gestos.items()), 2)

# Variáveis do estado do jogo
perguntas = nova_sequencia()     # Perguntas sorteadas
etapa = 0                        # Etapa atual (0 ou 1)
acertou = False                  # Flag de sucesso
ultimo_gesto = None             # Guarda o último gesto detectado
comando_h_enviado = False       # Controle para não enviar 'H' mais de uma vez

# Inicia captura da webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Espelha a imagem (efeito espelho)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Converte para RGB (exigido pelo MediaPipe)
    resultado = hands.process(rgb)  # Processa o reconhecimento de mãos

    # Seleciona a pergunta e resposta esperada da etapa atual
    texto_pergunta, resposta_esperada = perguntas[etapa]

    # Se alguma mão for detectada
    if resultado.multi_hand_landmarks:
        for handLms in resultado.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            gesto = reconhecer_gesto(handLms)

            # Só processa se for um novo gesto válido
            if gesto != "desconhecido" and gesto != ultimo_gesto:
                if gesto == resposta_esperada:
                    if etapa == 0:
                        arduino.write(b'Y')  # Concluiu 1ª etapa
                        time.sleep(0.5)
                    elif etapa == 1 and not comando_h_enviado:
                        arduino.write(b'H')  # Acertou metade da 2ª etapa
                        comando_h_enviado = True
                        time.sleep(0.5)

                    etapa += 1  # Avança para próxima etapa
                    if etapa >= len(perguntas):  # Se completou as 2 etapas
                        arduino.write(b'G')  # Envia comando de sucesso final
                        acertou = True
                        etapa = 0
                        comando_h_enviado = False
                        perguntas = nova_sequencia()  # Sorteia nova rodada
                        time.sleep(1.5)

                else:
                    # Resposta errada → reinicia
                    etapa = 0
                    comando_h_enviado = False
                    perguntas = nova_sequencia()
                    time.sleep(1)

                ultimo_gesto = gesto  # Atualiza o gesto mais recente

    # Exibe a pergunta e a etapa atual na tela
    cv2.putText(frame, f"{texto_pergunta}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    cv2.putText(frame, f"Etapa: {etapa + 1}/2", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Mostra "Acesso Liberado!" quando a sequência for correta
    if acertou:
        cv2.putText(frame, "Acesso Liberado!", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        acertou = False

    # Exibe a imagem da câmera com as informações desenhadas
    cv2.imshow("Quiz de Gestos - Porta Secreta", frame)

    # Encerra o programa se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a câmera e fecha a janela do OpenCV ao final
cap.release()
cv2.destroyAllWindows()
