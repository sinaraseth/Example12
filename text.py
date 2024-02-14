import pyrealsense2 as rs
import cv2

# Create a pipeline
pipeline = rs.pipeline()

# Create a configuration for the pipeline
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline with the given configuration
pipeline.start(config)

try:
    while True:
        # Wait for the next set of frames
        frames = pipeline.wait_for_frames()

        # Get the color frame
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert the color frame to a numpy array
        color_image = np.asanyarray(color_frame.get_data())

        # Display the color image
        cv2.imshow('RealSense Camera', color_image)

        # Wait for the 'q' key to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Stop the pipeline
    pipeline.stop()

# Close OpenCV windows
cv2.destroyAllWindows()
