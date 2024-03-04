import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

#TOP LEFT COORDINATES
area_x, area_y = 269, 0
area_width, area_height = 155, 152
nose = [4]
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks = True)

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cam.isOpened():

        _, frame = cam.read()

        frame = cv2.flip(frame, 1)
        
        cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 255, 0), 2)

        # Extract the fixed rectangle area from the frame
        selected_frame = frame[area_y:area_y + area_height, area_x:area_x + area_width]

        #selected_frame = cv2.flip(selected_frame, 1)
        frame_h, frame_w, _ = selected_frame.shape
        selected_frame = cv2.cvtColor(selected_frame, cv2.COLOR_BGR2RGB)
        output = facemesh.process(selected_frame)
        selected_frame = cv2.cvtColor(selected_frame, cv2.COLOR_RGB2BGR)
        landmark_points = output.multi_face_landmarks

        if landmark_points:
            landmarks = landmark_points[0].landmark
            nose = [landmarks[4]]
            for landmark in nose:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                #print(x, y)
                cv2.circle(frame, (x,y), 3, (0,255,0))
                screen_x = (screen_w/frame_w) * x
                screen_y = (screen_h/frame_h) * y
                pyautogui.moveTo(screen_x,screen_y)
            left_eye = [landmarks[145], landmarks[159]]
            left_eye = [landmarks[145], landmarks[159]]
            for landmark in left_eye:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x,y), 3, (0,255,255))
                print(left_eye[0].y - left_eye[1].y)
            if (left_eye[0].y - left_eye[1].y) < 0.042:
                pyautogui.click()
                pyautogui.sleep(1)

        
        cv2.imshow('Eye Controlled Mouse', selected_frame)
    
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break