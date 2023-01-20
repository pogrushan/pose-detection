import mediapipe as mp
import tkinter as tk
import numpy as np
import cv2, os

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

#make a window to display coordinates
window = tk.Tk()
window.title("Coordinates")
window.geometry("500x500")

def mediapipe_detection(showimage, results):

    # 2. Right hand landmarks
    mp_drawing.draw_landmarks(showimage, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
    )

    # 3. Left Hand landmarks
    mp_drawing.draw_landmarks(showimage, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
    )

    # 4. Pose Detections
    mp_drawing.draw_landmarks(showimage, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
    )

    return image

cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    while cap.isOpened():

        os.system('cls')
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = holistic.process(image)

        try: 
            x = results.right_hand_landmarks.landmark.x
            y = results.right_hand_landmarks.landmark.y
            z = results.right_hand_landmarks.landmark.z
            print('Right hand landmarks: ')
            print("                     x: ", x)
            print("                     y: ", y)
            print("                     z: ", z)
            #show coordinates in window
            label = tk.Label(window, text="Right Hand: showimage          x: " + str(x) + "showimage          y: " + str(y) + "showimage          z: " + str(z))
            label.pack()
            window.update()
        except: pass
        try: 
            x = results.left_hand_landmarks.landmark.x
            y = results.left_hand_landmarks.landmark.y
            z = results.left_hand_landmarks.landmark.z
            print('Left hand landmarks: ')
            print("                     x: ", x)
            print("                     y: ", y)
            print("                     z: ", z)
            with open("coordinates.txt", "w") as f:
                f.write("x: " + str(x) + "y: " + str(y) + "z: " + str(z))
            label2 = tk.Label(window, text="Left Hand: showimage          x: " + str(x) + "showimage          y: " + str(y) + "showimage          z: " + str(z))
            label2.pack()
            window.update()
        except: pass
        try: 
            x = results.pose_landmarks.landmark.x
            y = results.pose_landmarks.landmark.y
            z = results.pose_landmarks.landmark.z
            print('Pose landmarks: ')
            print("                     x: ", x)
            print("                     y: ", y)
            print("                     z: ", z)
            label3 = tk.Label(window, text="Pose:          x: " + str(x) + "         y: " + str(y) + "          z: " + str(z))
            label3.pack()
            window.update()
        except: pass

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        image = mediapipe_detection(image, results)

        cv2.imshow('Camera', image)
        window.update()

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

window.destroy()
cap.release()
cv2.destroyAllWindows()