from imutils import face_utils
import numpy as np
import argparse
import imutils
import pyautogui
import dlib
import cv2


detector = dlib.get_frontal_face_detector() #dlib에서 해당 함수를 사용
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #사람의 얼굴에 68개의 점을 찍어 놓은 데이터를 저장하고 있는 face68을 사용한다

cap = cv2.VideoCapture(0) #opencv함수, 1번비디오인 웹캠을 사용한다는 의미

def extract_eye(image, left, bottom_left, bottom_right, right, upper_right, upper_left):
	lower_bound = max([left[1], right[1], bottom_left[1], bottom_right[1], upper_left[1], upper_right[1]])
	upper_bound = min([left[1], right[1], upper_left[1], upper_right[1], bottom_left[1], bottom_right[1]])

	eye = image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3]

	image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3] = eye


	return eye

while(True):
	# 이미지를 불러와 회색으로 바꾸어준다
	ret, image = cap.read()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# 회색으로 바꾼 이미지에서 얼굴을 찾는다
	rects = detector(gray, 1)

	# 얼굴인식을 위한 loop문, frame단위로 얼굴을 인식하고 아래 문장을 통하여 동공의 중심을 찾는다
	for (i, rect) in enumerate(rects):
		# 68개의 점에서 landmark를 numpy를 사용하여 array형태로 바꾸어준다
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)




		count = 1
		right_eye = imutils.resize(extract_eye(image, shape[36], shape[41], shape[46], shape[45], shape[44], shape[37]), width=360, height=240)
		#left_eye = imutils.resize(extract_eye(image, shape[42], shape[47], shape[46], shape[45], shape[44], shape[43]), width=100, height=50)

		rows, cols, _ = right_eye.shape
		gray_right_eye = cv2.cvtColor(right_eye, cv2.COLOR_BGR2GRAY)
		gray_right_eye = cv2.GaussianBlur(gray_right_eye, (7, 7), 0)

		_, threshold = cv2.threshold(gray_right_eye, 40, 255, cv2.THRESH_BINARY_INV)
		contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

		cv2.line(right_eye,(250,300),(250,400),(255,0,0),1)
		cv2.line(right_eye,(200,350),(300,350),(255,0,0),1)
		for cnt in contours:
			(x, y, w, h) = cv2.boundingRect(cnt)

			#cv2.drawContours(right_eye, [cnt], -1, (0, 0, 255), 3)
			cv2.rectangle(right_eye, (x, y), (x + w, y + h), (255, 0, 0), 2)
			cv2.line(right_eye, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
			cv2.line(right_eye, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)

		cv2.imshow("Threshold", threshold)
		cv2.imshow("gray right_eye", gray_right_eye)
		cv2.imshow("right_eye", right_eye)



		#눈 테두리에 위치한 36~41번, 42~47번에 점을 찍어서 눈의 위치를 표시해준다
		for (x, y) in shape:

			if count > 36 and count < 43:
				cv2.circle(image, (x, y), 1, (255, 0, 0), -1)
			if count > 42 and count < 49:
				cv2.circle(image, (x, y), 1, (255, 0, 0), -1)

			count += 1


		image[0:len(right_eye),0:len(right_eye[0])] = right_eye
		#image[0:len(left_eye),0:len(left_eye[0])] = left_eye

	cv2.imshow("eye", right_eye)


	key = cv2.waitKey(1)
	if key == 27:
		break


cap.release()
cv2.destroyAllWindows()
