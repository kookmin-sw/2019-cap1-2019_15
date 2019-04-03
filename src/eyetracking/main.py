import cv2
import numpy as np
import dlib
import pyautogui

green = (0, 255, 0)

#카메라로부터 비디오 캡쳐 객체를 생성, 0번이므로 기본 카메라
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def xmidpoint(p1, p2):
    return int((p1.x + p2.x)/2)

def ymidpoint(p1, p2):
    return int((p1.y + p2.y)/2)




while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        leftpts = np.array([[landmarks.part(36).x, landmarks.part(36).y], [landmarks.part(37).x, landmarks.part(37).y], [landmarks.part(38).x, landmarks.part(38).y], [landmarks.part(39).x, landmarks.part(39).y], [landmarks.part(40).x, landmarks.part(40).y], [landmarks.part(41).x, landmarks.part(41).y]], np.int32)
        rightpts = np.array([[landmarks.part(42).x, landmarks.part(42).y], [landmarks.part(43).x, landmarks.part(43).y], [landmarks.part(44).x, landmarks.part(44).y], [landmarks.part(45).x, landmarks.part(45).y], [landmarks.part(46).x, landmarks.part(46).y], [landmarks.part(47).x, landmarks.part(47).y]], np.int32)

        leftpts = leftpts.reshape((-1, 1, 2))
        rightpts = rightpts.reshape((-1, 1, 2))

        cv2.polylines(frame, [leftpts], True, green, 2)
        cv2.polylines(frame, [rightpts], True, green, 2)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
