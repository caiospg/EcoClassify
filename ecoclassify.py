from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    results = model(frame)

    cv2.imshow("Detecção", results[0].plot())

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()