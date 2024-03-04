import cv2
import mediapipe as mp
import pyautogui

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
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[4:5]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            print(x, y)
            cv2.circle(frame, (x,y), 3, (0,255,0))
            if id == 0:
                screen_x = (screen_w/frame_w) * x
                screen_y = (screen_h/frame_h) * y
                pyautogui.moveTo(screen_x,screen_y)
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 3, (0,255,255))
        if (left_eye[0].y - left_eye[1].y) < 0.009:
            pyautogui.doubleClick()
            print(left_eye[0].y - left_eye[1].y)
            pyautogui.sleep(1)
        right_eye = [landmarks[475], landmarks[477]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x,y), 3, (255,255,255))
        #if (right_eye[0].y - right_eye[1].y) < 0.010:
            #pyautogui.doubleClick()
            #pyautogui.sleep(1)
        
        
    
        cv2.imshow('Eye Controlled Mouse', frame)

        if cv2.waitKey(10) & 0xFF == ord('c'):
            break