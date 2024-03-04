import cv2
import mediapipe as mp
import pyautogui

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
cam = cv2.VideoCapture(0)

nose = [5]

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cam.isOpened():

        _, frame = cam.read()

        area_x, area_y = 202, 47  # Coordinates of the top-left corner of the area
        area_width, area_height = 192, 101  # Size of the area  

        frame = cv2.flip(frame, 1)
        
        cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 255, 0), 2)

        # Extract the fixed rectangle area from the frame
        selected_frame = frame[area_y:area_y + area_height, area_x:area_x + area_width]
        #selected_frame = cv2.flip(selected_frame, 1)
        frame_h, frame_w, _ = selected_frame.shape
        selected_frame = cv2.cvtColor(selected_frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(selected_frame)
        selected_frame = cv2.cvtColor(selected_frame, cv2.COLOR_RGB2BGR)


        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(selected_frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec = mp_drawing.DrawingSpec(color=(255,102,102),thickness=1,circle_radius=1),
                    connection_drawing_spec = mp_drawing.DrawingSpec(color=(102,204,0),thickness=1,circle_radius=1))
        except:
            pass


        cv2.imshow('Camera',selected_frame)
        cv2.imshow('Camera maior',frame)

        if cv2.waitKey(10) & 0xFF == ord('c'):
            break