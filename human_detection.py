import cv2
import bt_tester
import numpy
ped_detector = cv2.CascadeClassifier('hogcascade_pedestrians.xml')
fac_detector = cv2.CascadeClassifier('haarcascade_upperbody.xml')
#import timeit


def main():
	windowName = "LIve Video Feed"
	cv2.namedWindow(windowName)
	cap = cv2.VideoCapture(0)
	
	cap.set(3, 400)
	cap.set(4, 300)
	
        if cap.isOpened():
                ret, frame = cap.read()
        else:
                ret = False
	
	body_average = 0
	face_average = 0
	body_sqsum = 0
	face_sqsum = 0
	loopdiv = 0
	clock = 0
	#start = timeit.timeit()

	while ret:
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		body = ped_detector.detectMultiScale(gray, 3, 2)
		face = fac_detector.detectMultiScale(gray, 2, 3)

		for (x, y, w, h) in body:
			cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
			#print("a" + str(len(body)))
		for (x, y, w, h) in face:
			cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 0, 255), 2)
		body_sqsum += len(body)
		face_sqsum += len(face)
		if clock%3 == 0:
			body_average = body_sqsum / 3.0
			face_average = face_sqsum / 3.0
			print("Body: "+str(body_average))
			print("Face: "+str(face_average))
			print(" \n Final Calc: " + str(body_average+face_average))
			loopdiv = 0
			body_sqsum = 0
			face_sqsum = 0
			print(" num of strangers: " + count())		
			
		cv2.imshow(windowName, gray)
		if cv2.waitKey(1) == 27:
			break
		
		loopdiv += 1
		clock += 1
	cv2.destroyWindow(windowName)

        cap.release()

if __name__ == "__main__":
        main()

