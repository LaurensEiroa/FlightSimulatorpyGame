import cv2
from picamera2 import Picamera2

class Camera:
    def __init__(self):
        # Initialize Picamera2
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_still_configuration())
        self.picam2.start()

    def get_frame(self):
        # Capture a frame
        frame = self.picam2.capture_array()
        return frame

    def release(self):
        # Stop the camera
        self.picam2.stop()

if __name__ == "__main__":
    camera = Camera()

    try:
        while True:
            frame = camera.get_frame()
            # Display the frame (optional)
            cv2.imshow("Frame", frame)

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
