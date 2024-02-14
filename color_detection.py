import cv2
import pyrealsense2 as rs
import numpy as np

# color
# red_lower = np.array([170, 100, 100])
# red_upper = np.array([180, 255, 255])

# green_lower = np.array([0,240,0])
# green_upper = np.array([0,255,0])

# blue_lower = np.array([240, 0, 0])
# blue_upper = np.array([255, 0, 0])

# original color
red_lower = np.array([170, 100, 100])
red_upper = np.array([180, 255, 255])

green_lower = np.array([35,50,50])
green_upper = np.array([90,255,255])

blue_lower = np.array([103, 100, 100])
blue_upper = np.array([128, 255, 255])

# Default configuration


# pipeline_wrapper = rs.pipeline_profile(pipeline)


# def release(self):
#     self.pipeline.stop()


cv2.namedWindow("Color frame")
pipeline = rs.pipeline()
config = rs.config()

pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

while True:

    frames = pipeline.wait_for_frames()
    
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    color_image = np.asanyarray(color_frame.get_data())

    hsv_frame = cv2.cvtColor(color_image, cv2.COLOR_HSV2BGR)

    mask_red = cv2.inRange(hsv_frame, red_lower, red_upper)
    mask_green = cv2.inRange(hsv_frame, green_lower, green_upper)
    mask_blue = cv2.inRange(hsv_frame, blue_lower, blue_upper)


    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ =cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

    for color, color_mask, color_bgr in zip(["Red", "Green", "Blue"],
                                            [mask_red, mask_green, mask_blue],
                                            [(0, 0, 255), (0, 255, 0),
                                             (255, 0, 0)]):
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(color_image, (x,y), (x + w, y + h), color_bgr, 2)

    cv2.imshow("Color frame", color_image)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break
