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


    y_indices, x_indices = np.indices((altura, largura))

    coordenadas = np.stack((x_indices.ravel(), y_indices.ravel()), axis=0)


    coordenadas_centradas = coordenadas - np.array([[centro[0]], [centro[1]]])


    coordenadas_rotacionadas = R @ coordenadas_centradas


    coordenadas_final = coordenadas_rotacionadas + np.array([[centro[0]], [centro[1]]])


    x_rot = coordenadas_final[0, :].reshape((altura, largura)).astype(int)
    y_rot = coordenadas_final[1, :].reshape((altura, largura)).astype(int)


    imagem_rotacionada = np.zeros_like(imagem)


    valid_mask = (
        (x_rot >= 0) & (x_rot < largura) &
        (y_rot >= 0) & (y_rot < altura)
    )


    imagem_rotacionada[y_indices[valid_mask], x_indices[valid_mask]] = \
        imagem[y_rot[valid_mask], x_rot[valid_mask]]

    return imagem_rotacionada

def run():

    cap = cv.VideoCapture(0)


    width = 320
    height = 240

    if not cap.isOpened():
        print("Não consegui abrir a câmera!")
        exit()

    angulo = 0

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Não consegui capturar frame!")
            break

        frame = cv.resize(frame, (width, height), interpolation=cv.INTER_AREA)
        image = frame.astype(float) / 255.0


        angulo_rad = np.radians(angulo)

        rotacionada = rotacionar(image, angulo_rad)

        cv.imshow('Video Rotacionado', rotacionada)

        angulo = (angulo + 1) % 360  

        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


run()
