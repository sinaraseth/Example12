import cv2
import pyrealsense2 as rs
import numpy as np 

# color
blue_lower = np.array([103, 100, 100])
blue_upper = np.array([128, 255, 255])


# camera configuration
cv2.namedWindow("Color frame")
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

def get_frame():
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    if not color_frame:
        return False, None, None
    return True, depth_image, color_image


while True:
    ret, depth_frame,color_frame = get_frame()

    hsv_frame = cv2.cvtColor(color_frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:
            # detect color
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(color_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # detect distance
            cv2.circle(color_frame, (x, y), 4, (255, 0, 0))
            distance = depth_frame[x, y]
            cv2.putText(color_frame, "{}mm".format(distance), (x, y - 20), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow('frame', color_frame)

    if cv2.waitKey(1) & 0xFF == ord('d'):
        break

cv2.destroyAllWindows()        
    

    
