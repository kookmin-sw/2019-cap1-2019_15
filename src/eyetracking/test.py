from imutils import face_utils
import numpy as np
import argparse
import imutils
import pyautogui
import dlib
import cv2


detector = dlib.get_frontal_face_detector() #dlib에서 해당 함수를 사용
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #사람의 얼굴에 68개의 점을 찍어 놓은 데이터를 저장하고 있는 face68을 사용한다

cap = cv2.VideoCapture(1) #opencv함수, 1번비디오인 웹캠을 사용한다는 의미

past_values_x = [] #past value를 저장하는 array생성
def min_intensity_x(img): #x값의 떨림 정도를 파악
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #이미지를 gray컬러로 변경

	min_sum_y = 255 * len(img)
	min_index_x = -1

	for x in range(len(img[0])):

		temp_sum_y = 0

		for y in range(len(img)):
			temp_sum_y += img[y][x]

		if temp_sum_y < min_sum_y:
			min_sum_y = temp_sum_y
			min_index_x = x

	past_values_x.append(min_index_x)

	if len(past_values_x) > 3:
		past_values_x.pop(0)

	return int(sum(past_values_x) / len(past_values_x))

past_values_y = []
def min_intensity_y(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


	min_sum_x = 255 * len(img[0])
	min_index_y = -1

	for y in range(len(img)):

		temp_sum_x = 0

		for x in range(len(img[0])):
			temp_sum_x += img[y][x]

		if temp_sum_x < min_sum_x:
			min_sum_x = temp_sum_x
			min_index_y = y

	past_values_y.append(min_index_y)
	if len(past_values_y) > 3:
		past_values_y.pop(0)

	return int(sum(past_values_y) / len(past_values_y))

def extract_eye(image, left, bottom_left, bottom_right, right, upper_right, upper_left):
	lower_bound = max([left[1], right[1], bottom_left[1], bottom_right[1], upper_left[1], upper_right[1]])
	upper_bound = min([left[1], right[1], upper_left[1], upper_right[1], bottom_left[1], bottom_right[1]])

	eye = image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3]

	pupil_x = min_intensity_x(eye)
	pupil_y = min_intensity_y(eye)
	cv2.circle(eye,(pupil_x, pupil_y), 2, (0,255,0), -1)

	cv2.line(image,(int((bottom_left[0] + bottom_right[0]) / 2), lower_bound), (int((upper_left[0] + upper_right[0]) / 2), upper_bound),(0,0,255), 1)
	cv2.line(image,(left[0], left[1]), (right[0], right[1]),(0,0,255), 1)



	image[upper_bound-3:lower_bound+3, left[0]-3:right[0]+3] = eye


	return eye

while(True):
	# 이미지를 불러와 회색으로 바꾸어준다
	ret, image = cap.read()
	image = imutils.resize(image, width=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# 회색으로 바꾼 이미지에서 얼굴을 찾는다
	rects = detector(gray, 1)

	# 얼굴인식을 위한 loop문, frame단위로 얼굴을 인식하고 아래 문장을 통하여 동공의 중심을 찾는다
	for (i, rect) in enumerate(rects):
		# 68개의 점에서 landmark를 numpy를 사용하여 array형태로 바꾸어준다
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)




		count = 1
		right_eye = imutils.resize(extract_eye(image, shape[36], shape[41], shape[40], shape[39], shape[38], shape[37]), width=100, height=50)
		left_eye = imutils.resize(extract_eye(image, shape[42], shape[47], shape[46], shape[45], shape[44], shape[43]), width=100, height=50)



		#눈 테두리에 위치한 36~41번, 42~47번에 점을 찍어서 눈의 위치를 표시해준다
		for (x, y) in shape:

			if count > 36 and count < 43:
				cv2.circle(image, (x, y), 1, (255, 0, 0), -1)
			if count > 42 and count < 49:
				cv2.circle(image, (x, y), 1, (255, 0, 0), -1)

			count += 1


		image[0:len(right_eye),0:len(right_eye[0])] = right_eye
		image[0:len(left_eye),0:len(left_eye[0])] = left_eye

	cv2.imshow("Frame", image)


	key = cv2.waitKey(1)
	if key == 27:
		break


cap.release()
cv2.destroyAllWindows()
