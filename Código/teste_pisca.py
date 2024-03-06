import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
screen_w, screen_h = pyautogui.size()
#print(screen_h, screen_w)
area_x, area_y = 260, 130  # Coordinates of the top-left corner of the area
area_width, area_height = 110, 154  # Size of the area

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    #rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #output = face_mesh.process(rgb_frame)
    #landmark_points = output.multi_face_landmarks
    #frame_h, frame_w, _ = frame.shape
    
    # Create a rectangle with the areas that our nose pass.
    cv2.rectangle(frame, (area_x, area_y), (area_x + area_width, area_y + area_height), (0, 0, 255), 2)

        # Extract the fixed rectangle area from the frame
    selected_frame = frame[area_y:area_y + area_height, area_x:area_x + area_width]
    frame_hn, frame_wn, _ = selected_frame.shape
    nose_rgb = cv2.cvtColor(selected_frame, cv2.COLOR_BGR2RGB)
    output_nose = face_mesh.process(nose_rgb)
    landmark_nose = output_nose.multi_face_landmarks

    # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # output = face_mesh.process(rgb_frame)
    # landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    
    if landmark_nose:
        landmarks = landmark_nose[0].landmark
        nose = [landmarks[5]]
        for id, landmark in enumerate(nose):
            x = int(landmark.x * frame_wn)
            y = int(landmark.y * frame_hn)
            cv2.circle(frame, (x,y), 3, (0,255,0))
            #print(x,y)
            #print(landmark.x, landmark.y)
            if id == 0:
                screen_x = (screen_w/frame_wn) * int(landmark.x * frame_wn)
                screen_y = (screen_h/frame_hn) * int(landmark.y * frame_hn)
                pyautogui.moveTo(screen_x,screen_y)
             #   print(screen_x,screen_y)
        left_eye = [landmarks[158], landmarks[153]]
        # for landmark in left_eye:
        #     x = int(landmark.x * frame_wn)
        #     y = int(landmark.y * frame_hn)
        #     cv2.circle(selected_frame, (x,y), 1, (0,255,255), -1)
        #     print(left_eye[1].y - left_eye[0].y)
        # if (left_eye[1].y - left_eye[0].y) < 0.005:
        #     for m_x, m_y in pyautogui.position():
        #         if area_x < m_x < area_x+30 and area_y < m_y < area_y+30:
        #             pyautogui.write('w')
        #             pyautogui.sleep(1)
        #     pyautogui.Click()
        #     pyautogui.sleep(1)
        right_eye = [landmarks[387], landmarks[390]]
        for landmark in right_eye:
            x = int(landmark.x * frame_wn)
            y = int(landmark.y * frame_hn)
            cv2.circle(selected_frame, (x,y), 1, (0,255,255), -1)
            print((right_eye[1].y - right_eye[0].y))
            #print(right_eye[0].y, right_eye[1].y)
        if (right_eye[1].y - right_eye[0].y) < 0.022: #=
            pyautogui.click()
            pyautogui.sleep(1)
    cv2.imshow('Selected Area', selected_frame)
    cv2.imshow('Eye Controlled Mouse', frame)
    if cv2.waitKey(10) & 0xFF == ord('c'):
        break