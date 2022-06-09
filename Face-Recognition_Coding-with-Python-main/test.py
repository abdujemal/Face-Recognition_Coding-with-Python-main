import cv2

cap = cv2.VideoCapture("https://192.168.43.135:8080/video")

while True:
    ret, frame = cap.read()

    cv2.imshow("Go test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break