from imutils import face_utils
import cv2
import numpy as np
import dlib
import pyautogui
import argparse
import imutils

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True, help="path to facial landmark predictor")

args = vars(ap.parse_args())


#카메라로부터 비디오 캡쳐 객체를 생성, 0번이므로 기본 카메라
cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

'''
def xmidpoint(p1, p2):
    return int((p1.x + p2.x)/2)

def ymidpoint(p1, p2):
    return int((p1.y + p2.y)/2)
'''

past_values_x = []

def min_x(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    min_sum_y = 255 * len(img)
    min_index_x = -1

    for x in range(len(img[0])):

        temp_y = 0

        for y in range(len(img)):
            temp_y += img[y][x]

        if temp_y < min_sum_y:
            min_sum_y = temp_y
            min_index_x = x

    past_values_x.append(min_index_x)

    if len(past_values_x) > 3:
        past_values_x.pop(0)

    return int(sum(past_values_x) / len(past_values_x))

past_values_y = []
def min_y(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    min_sum_x = 255 * len(img[0])
    min_index_y = -1

    for y in range(len(img)):

        temp_x = 0

        for x in range(len(img[0])):
            temp_x += img[y][x]

        if temp_x < min_sum_x:
            min_sum_x = temp_x
            min_index_y = y

    past_values_y.append(min_index_y)

    if len(past_values_y) > 3:
        past_values_y.pop(0)

    return int(sum(past_values_y) / len(past_values_y))


def detect_eye(image, left, bottom_left, bottom_right, right, upper_right, upper_left):
    lower_bound = max([left[1], right[1], bottom_left[1], bottom_right[1], upper_left[1], upper_right[1]])
    upper_bound = min([left[1], right[1], upper_left[1], upper_right[1], bottom_left[1], bottom_right[1]])

    eye = image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3]

    pupil_x = min_x(eye)
    pupil_y = min_y(eye)

    #cv2.circle(eye,(pupil_x, pupil_y), 3, (255,0,0), -1)
    cv2.line(eye,(pupil_x,0),(pupil_x,len(eye)),(0,255,0), 1)
    cv2.line(eye,(0,pupil_y),(len(eye[0]),pupil_y),(0,255,0), 1)


    cv2.line(image, (int((bottom_left[0] + bottom_right[0]) / 2), lower_bound), (int((upper_left[0] + upper_right[0]) / 2), upper_bound),(0,0,255), 1)
    cv2.line(image, (left[0], left[1]), (right[0], right[1]),(0,0,255), 1)

    image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3] = eye
    return eye





while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frame = imutils.resize(frame, width=500)

    faces = detector(gray, 1)

    for(i, face) in enumerate(faces):
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        count = 1
        right_eye = imutils.resize(detect_eye(frame, shape[36], shape[41], shape[40], shape[39], shape[38], shape[37]), width=100, height=50)

        for(x, y) in shape:
            if count > 36 and count < 43:
                cv2.circle(frame, (x, y), 1, (255,0,0), -1)

            count += 1

        frame[0:len(right_eye), 0:len(right_eye[0])] = right_eye

    '''
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        leftpts = np.array([[landmarks.part(36).x, landmarks.part(36).y], [landmarks.part(37).x, landmarks.part(37).y], [landmarks.part(38).x, landmarks.part(38).y], [landmarks.part(39).x, landmarks.part(39).y], [landmarks.part(40).x, landmarks.part(40).y], [landmarks.part(41).x, landmarks.part(41).y]], np.int32)
        rightpts = np.array([[landmarks.part(42).x, landmarks.part(42).y], [landmarks.part(43).x, landmarks.part(43).y], [landmarks.part(44).x, landmarks.part(44).y], [landmarks.part(45).x, landmarks.part(45).y], [landmarks.part(46).x, landmarks.part(46).y], [landmarks.part(47).x, landmarks.part(47).y]], np.int32)

        leftpts = leftpts.reshape((-1, 1, 2))
        rightpts = rightpts.reshape((-1, 1, 2))

        cv2.polylines(frame, [leftpts], True, green, 2)
        cv2.polylines(frame, [rightpts], True, green, 2)
        '''


    cv2.imshow("Frame", frame)


    key = cv2.waitKey(1)
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()
