import cv2

cap = cv2.VideoCapture(0)
ret, img = cap.read()
cv2.imshow('windowname', img)
cv2.waitKey(0)

cap.release()

