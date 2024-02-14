import cv2
import pyrealsense2
# from color_realsense_depth import *

# color
blue_lower = np.array([103, 100, 100])
blue_upper = np.array([128, 255, 255])

# Define the target point
point = (320, 240)
# Initialize Camera Intel Realsense
dc = DepthCamera()

# Create mouse event
cv2.namedWindow("Color frame")

while True:

    ret, depth_frame, color_frame = dc.get_framed()

    hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

    # mask = cv2.inRange(hsv_frame, green_lower, green_upper)
    mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # cv2.imshow("depth frame", depth_frame)
    cv2.imshow("Color frame", color_frame)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break