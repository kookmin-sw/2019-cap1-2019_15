from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from pymouse import PyMouse
m = PyMouse()


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(1)

def extract_eye(image, left, bottom_left, bottom_right, right, upper_right, upper_left):
	lower_bound = max([left[1], right[1], bottom_left[1], bottom_right[1], upper_left[1], upper_right[1]])
	upper_bound = min([left[1], right[1], upper_left[1], upper_right[1], bottom_left[1], bottom_right[1]])

	eye = image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3]

	image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3] = eye


	return eye

while(True):

	ret, image = cap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


	rects = detector(gray, 1)

	for (i, rect) in enumerate(rects):
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)




		count = 1
		right_eye = imutils.resize(extract_eye(image, shape[36], shape[41], shape[46], shape[45], shape[44], shape[37]), width=200, height=100)
		#left_eye = imutils.resize(extract_eye(image, shape[42], shape[47], shape[46], shape[45], shape[44], shape[43]), width=200, height=100)

		rows, cols, _ = right_eye.shape
        right_eye = right_eye[0:30,0:70] # cut right_eye

        gray_right_eye = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
        gray_right_eye = cv2.GaussianBlur(gray_right_eye, (7, 7), 0)
        _, threshold = cv2.threshold(gray_right_eye, 45, 255, cv2.THRESH_BINARY_INV)
        _, contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

        cv2.line(right_eye,(250,300),(250,400),(255,0,0),1)
        cv2.line(right_eye,(200,350),(300,350),(255,0,0),1)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
			#cv2.drawContours(right_eye, [cnt], -1, (0, 0, 255), 3)
            cv2.rectangle(right_eye, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.line(right_eye, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
            cv2.line(right_eye, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
            print((int(x)+int(w/2)))
            print((int(y)+int(h/2)))

            #move mouse
            xx = list(m.position())
            xxx = xx[0]
            yyy = xx[1]
            if((int(x)+int(w/2)) < 30 ):
                m.move(xxx + 20,yyy)
            if((int(x)+int(w/2)) > 41 ):
                m.move(xxx - 20,yyy)
                
        cv2.imshow("Threshold", threshold)
        cv2.imshow("gray right_eye", gray_right_eye)
        cv2.imshow("right_eye", right_eye)


		# for (x, y) in shape:
        #
		# 	if count > 36 and count < 43:
		# 		cv2.circle(image, (x, y), 1, (255, 0, 0), -1)
		# 	if count > 42 and count < 49:
		# 	 	cv2.circle(image, (x, y), 1, (255, 0, 0), -1)
        #
		# 	count += 1
        #
		# #image[0:len(left_eye),0:len(left_eye[0])] = left_eye
		# right_eye[0:len(right_eye),0:len(right_eye[0])] = right_eye
        #
        # cv2.imshow("eye", right_eye)


	key = cv2.waitKey(1)
	if key == 27:
		break


cap.release()
cv2.destroyAllWindows()
