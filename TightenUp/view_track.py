import cv2
import numpy as np
from track_generator import generatePolygon


img_size = (600,600, 1)
center = (int(img_size[0]/2), int(img_size[1]/2))
rad = img_size[0] / 4
irreg = 0.8
spike = 0.25
n = 8

while True:
    points = generatePolygon(center[0], center[1], rad, irreg, spike, n)
    points.append(points[0])

    img = np.zeros(img_size, dtype=np.uint8)
    for i in range(n):
        cv2.line(img, points[i], points[i+1], 255, 50)

    for i, p in enumerate(points[:-1]):
        img = cv2.putText(img, str(i), p, cv2.FONT_HERSHEY_SIMPLEX , 1, 0)

    cv2.imshow("track", img)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break