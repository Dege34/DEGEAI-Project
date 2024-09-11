import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import cv2
import mediapipe as mp
import numpy as np
from tkinter import filedialog
import tkinter as tk


mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


overlay_image = None
overlay_landmarks = None

def initialize_camera():
    return cv2.VideoCapture(0)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
def initialize_models():
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
    return hands, face_mesh

def eye_aspect_ratio(landmarks, eye_indices):
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    v1 = ((landmarks[eye_indices[1]].x - landmarks[eye_indices[5]].x)**2 + 
          (landmarks[eye_indices[1]].y - landmarks[eye_indices[5]].y)**2)**0.5
    v2 = ((landmarks[eye_indices[2]].x - landmarks[eye_indices[4]].x)**2 + 
          (landmarks[eye_indices[2]].y - landmarks[eye_indices[4]].y)**2)**0.5
    

    h = ((landmarks[eye_indices[0]].x - landmarks[eye_indices[3]].x)**2 + 
         (landmarks[eye_indices[0]].y - landmarks[eye_indices[3]].y)**2)**0.5
    

    return (v1 + v2) / (2.0 * h)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
def count_fingers(hand_landmarks):
    fingertips = [4, 8, 12, 16, 20]  
    count = 0
    for tip in fingertips:#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
    return count
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
def load_image(face_mesh):
    global overlay_image, overlay_landmarks
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        overlay_image = cv2.imread(file_path)
        if overlay_image is not None:
            overlay_rgb = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2RGB)
            overlay_results = face_mesh.process(overlay_rgb)
            if overlay_results.multi_face_landmarks:
                overlay_landmarks = overlay_results.multi_face_landmarks[0]
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
def apply_face_overlay(frame, face_landmarks):
    global overlay_image, overlay_landmarks
    if overlay_image is None or overlay_landmarks is None:
        return frame
    h, w = frame.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    
    points = np.array([(int(landmark.x * w), int(landmark.y * h)) for landmark in face_landmarks.landmark])
    hull = cv2.convexHull(points)
    cv2.fillConvexPoly(mask, hull, 255)
    
    oh, ow = overlay_image.shape[:2]
    overlay_points = np.array([(int(landmark.x * ow), int(landmark.y * oh)) for landmark in overlay_landmarks.landmark])
    
    M, _ = cv2.findHomography(overlay_points, points)
    warped_overlay = cv2.warpPerspective(overlay_image, M, (w, h))
    
    mask_inv = cv2.bitwise_not(mask)
    background = cv2.bitwise_and(frame, frame, mask=mask_inv)
    foreground = cv2.bitwise_and(warped_overlay, warped_overlay, mask=mask)
    result = cv2.add(background, foreground)
    
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    mp_drawing.draw_landmarks(
        image=result,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
    )
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    mp_drawing.draw_landmarks(
        image=result,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
    )#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    for idx, landmark in enumerate(face_landmarks.landmark):
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(result, (x, y), 1, (0, 255, 0), -1)
    
    return result

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 10 <= x <= 210 and param['frame'].shape[0] - 60 <= y <= param['frame'].shape[0] - 10:
            load_image(param['face_mesh'])

def main():
    cap = initialize_camera()
    hands, face_mesh = initialize_models()

    cv2.namedWindow('Hand and Face Tracking')

    while True:
        ret, frame = cap.read()
        if not ret:
            break


        cv2.setMouseCallback('Hand and Face Tracking', mouse_callback, {'face_mesh': face_mesh, 'frame': frame})

        if cv2.getTickCount() % 2 == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            hand_results = hands.process(rgb_frame)
            face_results = face_mesh.process(rgb_frame)
            #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    finger_count = count_fingers(hand_landmarks)
                    cv2.putText(frame, f'Fingers: {finger_count-1}', (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    if overlay_image is not None:
                        frame = apply_face_overlay(frame, face_landmarks)
                    else:
                        h, w = frame.shape[:2]#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
                        mask = np.zeros((h, w), dtype=np.uint8)
                        points = np.array([(int(landmark.x * w), int(landmark.y * h)) for landmark in face_landmarks.landmark])
                        hull = cv2.convexHull(points)
                        cv2.fillConvexPoly(mask, hull, 255)
                        green_overlay = np.zeros_like(frame)
                        green_overlay[:, :] = (0, 255, 0)
                        frame = cv2.addWeighted(frame, 1, cv2.bitwise_and(green_overlay, green_overlay, mask=mask), 0.3, 0)
                    
                    left_eye = [33, 160, 158, 133, 153, 144]
                    right_eye = [362, 385, 387, 263, 373, 380]
                    
                    left_ear = eye_aspect_ratio(face_landmarks.landmark, left_eye)
                    right_ear = eye_aspect_ratio(face_landmarks.landmark, right_eye)
                    
                    if left_ear < 0.2 and right_ear < 0.2:
                        print("Eyes closed, quitting application")
                        return
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        cv2.rectangle(frame, (10, frame.shape[0] - 60), (210, frame.shape[0] - 10), (0, 255, 0), -1)
        cv2.putText(frame, "Load Image", (20, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        text = "DegeAI"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = frame.shape[0] - 10

        cv2.rectangle(frame, (text_x - 10, text_y - text_size[1] - 10),
                      (text_x + text_size[0] + 10, text_y + 10), (0, 0, 0), -1)
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 0), font_thickness)

        cv2.imshow('Hand and Face Tracking', frame)
        #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    cap.release()
    cv2.destroyAllWindows()
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
if __name__ == "__main__":
    main()