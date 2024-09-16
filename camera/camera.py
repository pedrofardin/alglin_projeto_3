import numpy as np
import cv2 as cv
import math

def rotacionar(imagem, angulo):
    (altura, largura) = imagem.shape[:2]
    centro = (largura / 2, altura / 2)

    cos_theta = math.cos(angulo)
    sin_theta = math.sin(angulo)
    R = np.array([
        [cos_theta, -sin_theta],
        [sin_theta, cos_theta]
    ])

    y_indices, x_indices = np.indices((altura, largura)) # gerar coordenadas da imagem
    coordenadas = np.stack((x_indices.ravel(), y_indices.ravel()), axis=0) # transformar em matriz de coordenadas

    coordenadas_centradas = coordenadas - np.array([[centro[0]], [centro[1]]]) # transaladar para o centro
    coordenadas_rotacionadas = R @ coordenadas_centradas # rotacionar
    coordenadas_final = coordenadas_rotacionadas + np.array([[centro[0]], [centro[1]]]) # transladar de volta

    x_rot = coordenadas_final[0, :].reshape((altura, largura)).astype(int) # separar x
    y_rot = coordenadas_final[1, :].reshape((altura, largura)).astype(int) # separar y

    imagem_rotacionada = np.zeros_like(imagem) # criar imagem vazia

    valid_mask = (
        (x_rot >= 0) & (x_rot < largura) &
        (y_rot >= 0) & (y_rot < altura)
    ) # criar máscara para valores válidos (não dar out of bounds)

    imagem_rotacionada[y_indices[valid_mask], x_indices[valid_mask]] = \
        imagem[y_rot[valid_mask], x_rot[valid_mask]] # copiar valores

    return imagem_rotacionada

def cisalhar(imagem, fator_cisalhamento):
    (altura, largura) = imagem.shape[:2]
    S = np.array([
        [1, fator_cisalhamento],
        [0, 1]
    ])

    y_indices, x_indices = np.indices((altura, largura))
    coordenadas = np.stack((x_indices.ravel(), y_indices.ravel()), axis=0)

    coordenadas_cis = S @ coordenadas

    x_cis = coordenadas_cis[0, :].reshape((altura, largura)).astype(int)
    y_cis = coordenadas_cis[1, :].reshape((altura, largura)).astype(int)

    imagem_cisalhada = np.zeros_like(imagem)

    valid_mask = (
        (x_cis >= 0) & (x_cis < largura) &
        (y_cis >= 0) & (y_cis < altura)
    )

    imagem_cisalhada[y_indices[valid_mask], x_indices[valid_mask]] = \
        imagem[y_cis[valid_mask], x_cis[valid_mask]]

    return imagem_cisalhada

def run():
    # Essa função abre a câmera. Depois desta linha, a luz de câmera (se seu computador tiver) deve ligar.
    cap = cv.VideoCapture(0)

    width = 320
    height = 240

    # Aqui, defino a largura e a altura da imagem com a qual quero trabalhar.
    # Dica: imagens menores precisam de menos processamento!!!
    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    # Talvez o programa não consiga abrir a câmera. Verifique se há outros dispositivos acessando sua câmera!
    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    angulo = 0
    velocidade = 1  
    fator_cisalhamento = 0.0  

    # Esse loop é igual a um loop de jogo: ele encerra quando apertamos 'q' no teclado.
    while True:
        # Captura um frame da câmera
        ret, frame = cap.read()

        # A variável `ret` indica se conseguimos capturar um frame
        if not ret:
            print("Não consegui capturar frame!")
            break

        # Mudo o tamanho do meu frame para reduzir o processamento necessário
        # nas próximas etapas
        frame = cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)

        # A variável image é um np.array com shape=(width, height, colors)
        image = frame.astype(float) / 255.0

        #--------------------------------------#
        angulo_rad = np.radians(angulo)
        rotacionada = rotacionar(image, angulo_rad)
        imagem_final = cisalhar(rotacionada, fator_cisalhamento)
        #--------------------------------------#

        # Agora, mostrar a imagem na tela!
        cv.imshow('Video Transformado', imagem_final)

        angulo = (angulo + velocidade) % 360  

        key = cv.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('w'):  
            velocidade += 1
        elif key == ord('e'):
            velocidade -= 1
        elif key == ord('s'): 
            velocidade = max(1, velocidade - 1)
        elif key == ord('d'):  
            fator_cisalhamento += 0.1
        elif key == ord('a'):  
            fator_cisalhamento -= 0.1

    # Ao sair do loop, vamos devolver cuidadosamente os recursos ao sistema!
    cap.release()
    cv.destroyAllWindows()

run()