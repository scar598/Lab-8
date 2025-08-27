import cv2
import numpy as np


fly_img = cv2.imread('fly64.png')

if fly_img is None:
    print("Ошибка: изображение fly64.png не найдено!")
    exit()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Камера не найдена!")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка камеры")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray_frame, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


            center_x = x + w // 2
            center_y = y + h // 2


            fly_height, fly_width = fly_img.shape[:2]


            fly_x = center_x - fly_width // 2
            fly_y = center_y - fly_height // 2


            if (fly_x >= 0 and fly_y >= 0 and
                    fly_x + fly_width <= frame.shape[1] and
                    fly_y + fly_height <= frame.shape[0]):
                frame[fly_y:fly_y + fly_height, fly_x:fly_x + fly_width] = fly_img

    cv2.imshow('Marker Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()