import cv2
import mediapipe as mp
import pyautogui
import mouse
import time
import os
import numpy as np
from pynput.keyboard import Controller


cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
screen_w, screen_h = pyautogui.size()
resolucao_y = 1080
resolucao_x = 1920
BRANCO = (255,255,255)
PRETO = (0,0,0)
AZUL = (255,0,0)
VERDE = (0,255,0)
VERMELHO = (0,0,255)
AZUL_CLARO = (255,255,0)
offset = 50
#os.system("cmd /c start osk")

teclas = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A','S','D','F','G','H','J','K','L'],
            ['Z','X','C','V','B','N','M', ',','.',' ']]

teclado = Controller()
img_quadro = np.ones((resolucao_y, resolucao_x, 3), np.uint8)*255
cor_pincel = (255,0,0)
espessura_pincel = 7
x_quadro, y_quadro = 0, 0
contador = 0

def imprime_botoes(img, posicao, letra, tamanho = 50, cor_retangulo = BRANCO):
    cv2.rectangle(img, posicao, (posicao[0]+tamanho, posicao[1]+tamanho), cor_retangulo,cv2.FILLED)
    cv2.rectangle(img, posicao, (posicao[0]+tamanho, posicao[1]+tamanho), AZUL, 1)
    cv2.putText(img, letra, (posicao[0]+15,posicao[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, PRETO, 2)
    return img


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    frame = cv2.rectangle(frame)


    if landmark_points:
        landmarks = landmark_points[0].landmark
        left_eye = [landmarks[158], landmarks[153]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 1, (0,255,255), -1)
        #     print(left_eye[1].y - left_eye[0].y)
        # if (left_eye[1].y - left_eye[0].y) < 0.005:
        #     pyautogui.doubleClick()
        #     pyautogui.sleep(1)
        right_eye = [landmarks[385], landmarks[380]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 1, (0,255,255), -1)
            # print(right_eye[1].y - right_eye[0].y)
            #print(right_eye[0].y, right_eye[1].y)
        if (right_eye[1].y - right_eye[0].y) < 0.005:
            mouse.click()
            pyautogui.sleep(1)
        for id, landmark in enumerate(landmarks[4:5]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            #print(landmark.x, landmark.y)
            cv2.circle(frame, (x,y), 3, (0,255,0))
            if id == 0:
                screen_x = (screen_w/frame_w) * x
                screen_y = (screen_h/frame_h) * y
                pyautogui.moveTo(screen_x,screen_y)
        for indice_linha, linha_teclado in enumerate(teclas):
            for indice, letra in enumerate(linha_teclado):
                        
                frame = imprime_botoes(frame, (offset+indice*50, offset+indice_linha*50),letra)
                #print(offset+indice_linha*50, x, 100+indice_linha*50)
                        
                if offset+indice*50 < x < 100+indice*50 and offset + indice_linha*50< y <100+indice_linha*50:
                    frame = imprime_botoes(frame, (offset+indice*50, offset+indice_linha*50),letra, cor_retangulo=VERDE)
                if (left_eye[1].y - left_eye[0].y) < 0.005:
                    contador = 1
                    escreve = letra
                    frame = imprime_botoes(frame, (offset+indice*50, offset+indice_linha*50),letra, cor_retangulo=AZUL_CLARO)
                    
        if contador:
            contador+=1
            if contador == 3:
                print(contador)
                contador = 0
                teclado.press(escreve)
                print(escreve)
                    
                

    cv2.imshow('Eye Controlled Mouse', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break
