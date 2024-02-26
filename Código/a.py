import cv2
import mediapipe as mp
import pyautogui

screen_w, screen_h = pyautogui.size()
print(screen_w)
print(screen_h)


cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)
screen_w, screen_h = pyautogui.size()


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    print(frame_w)
    print(frame_h)
    cv2.imshow('Eye Controlled Mouse', frame)
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break