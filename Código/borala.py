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
area_x, area_y = 50, 120  # Coordinates of the top-left corner of the area
area_width, area_height = 30, 30  # Size of the area

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    w = cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 0, 255), 2)
    frame = w


    if landmark_points:
        landmarks = landmark_points[0].landmark
        left_eye = [landmarks[158], landmarks[153]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 1, (0,255,255), -1)
            #print(left_eye[1].y - left_eye[0].y)
        if (left_eye[1].y - left_eye[0].y) < 0.005:
            for m_x, m_y in pyautogui.position():
                if area_x < m_x < area_x+30 and area_y < m_y < area_y+30:
                    pyautogui.write('w')
                    pyautogui.sleep(1)
            pyautogui.doubleClick()
            pyautogui.sleep(1)
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
    cv2.imshow('Eye Controlled Mouse', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break