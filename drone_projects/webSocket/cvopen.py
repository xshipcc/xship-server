import cv2

cap = cv2.VideoCapture('rtsp://196.168.8.160:554/live/track0')

while(True):
     ret, frame = cap.read()
     cv2.imshow('frame',frame)
     if cv2.waitKey(1) & 0xFF == ord('q'):
         cv2.destroyAllWindows()
         break