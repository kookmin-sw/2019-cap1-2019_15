from imutils import face_utils
import numpy as np
from scipy.spatial import distance as dist
import argparse
import imutils
import dlib
import cv2
from pymouse import PyMouse
import time
m = PyMouse()



ANCHOR_POINT = (0, 0)

(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]


def eye_distance(eye):

	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])


	C = dist.euclidean(eye[0], eye[3])

	eye_dist = (A + B) / (2.0 * C)

	return eye_dist

EYE_AR_THRESH = 0.28
EYE_AR_CONSEC_FRAMES = 8
COUNTER = 0
TOTAL = 0

def direction(r_eye_point, anchor_point, w, h1, multiple=1):
	nx, ny = r_eye_point
	x, y = anchor_point

	if ny > y + multiple * h1:
		return 'down'
	elif ny < y - multiple * h1:
		return 'up'
	elif ny > y + multiple * h2:
		return 'down2'
	elif ny < y - multiple * h2:
		return 'up2'

	return '-'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

cap = cv2.VideoCapture(1)


def extract_eye(image, left, bottom_left, bottom_right, right, upper_right, upper_left):
	lower_bound = max([left[1], right[1], bottom_left[1], bottom_right[1], upper_left[1], upper_right[1]])
	upper_bound = min([left[1], right[1], upper_left[1], upper_right[1], bottom_left[1], bottom_right[1]])

	eye = image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3]

	image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3] = eye


	return eye

arr = []
ANCHOR = 0

while(True):
	ret, image = cap.read()
	image = image[150:480, 200:500]
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


	rects = detector(gray, 1)
	check = 0

	for (i, rect) in enumerate(rects):
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		r_eye = shape[nStart:nEnd]
		r_eye_point = (r_eye[4, 0], r_eye[4, 1])

		while ANCHOR < 10:
			ANCHOR += 1
			ANCHOR_POINT = r_eye_point






		x, y = ANCHOR_POINT
		nx, ny = r_eye_point
		w= 60
		h1= 4
		h2 =10
		h= 10
		multiple = 1
		cv2.line(image, ANCHOR_POINT, r_eye_point, (0,0,255), 2)

		dir = direction(r_eye_point, ANCHOR_POINT, w, h1)
		#cv2.putText(image, dir.upper(), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2) 3840
		drag = 18
		xx = list(m.position())
		xxx = xx[0]
		yyy = xx[1]
		if dir == 'up':
			m.move(xxx, 445)
		# elif dir == 'up2':
		# 	m.move(xxx,400)
		elif dir == 'down':
			m.move(xxx,1580)
		# elif dir == 'down2' :
		# 	m.move(xxx,3300)
		else :
			m.move(xxx,1065)



		leftEye = shape[lStart:lEnd]
		rightEye = shape[nStart:nEnd]
		leftEAR = eye_distance(leftEye)
		rightEAR = eye_distance(rightEye)


		ear = (leftEAR + rightEAR) / 2.0


		if ear < EYE_AR_THRESH:
			COUNTER += 1


		else:

			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				TOTAL += 1
				m.click(xxx,yyy,1)


			COUNTER = 0



		count = 1
		right_eye = imutils.resize(extract_eye(image, shape[36], shape[41], shape[46], shape[45], shape[44], shape[37]), width=200, height=100)
		#left_eye = imutils.resize(extract_eye(image, shape[42], shape[47], shape[46], shape[45], shape[44], shape[43]), width=200, height=100)

		rows, cols, _ = right_eye.shape
		right_eye = right_eye[0:1000,0:60] # cut right_eye

		gray_right_eye = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
		gray_right_eye = cv2.GaussianBlur(gray_right_eye, (25,25), 0)
		_, threshold = cv2.threshold(gray_right_eye, 30, 255, cv2.THRESH_BINARY_INV)
		contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

		cv2.line(right_eye,(250,300),(250,400),(255,0,0),1)
		cv2.line(right_eye,(200,350),(300,350),(255,0,0),1)
		# print(contours)

		# x = cv2.boundingRect(contours[0])
		# y = cv2.boundingRect(contours[1])
		# w = cv2.boundingRect(contours[2])
		# h = cv2.boundingRect(contours[3])

		for cnt in  contours :
			(x, y, w, h) = cv2.boundingRect(cnt)
			cv2.drawContours(right_eye, [cnt], -1, (0, 0, 255), 3)
			cv2.rectangle(right_eye, (x, y), (x + w, y + h), (255, 0, 0), 2)
			cv2.line(right_eye, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
			cv2.line(right_eye, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)

			print((int(x)+int(w/2)))

			#move mouse 19 4080

			arr.append((int(x)+int(w/2)))
			print(len(arr))
			if len(arr) == 20:
				a= np.array(arr)
				xx = list(m.position())
				xxx = xx[0]
				yyy = xx[1]
				#print(xx)
				avg = np.sort(a)

				if(avg[5] > 39 ):
					m.move(260,yyy)
				elif(avg[5] <= 35):
					m.move(790,yyy)
				else :
					m.move(540,yyy)
				arr.clear()


			break
			# for cnt in contour0s:
				# (x, y, w, h) = cv2.boundingRect(cnt)
				# print(cnt,"dddddddd")
				# print(x,y,w,h)




		check = 1
		cv2.imshow("Threshold", threshold)
		# #cv2.imshow("gray right_eye", gray_right_eye)
		# cv2.imshow("right_eye", right_eye)
		cv2.imshow("image",image)

	if check == 0:
		ANCHOR =0

	key = cv2.waitKey(1)
	if key == 27:
		break


cap.release()
cv2.destroyAllWindows()
