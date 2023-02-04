from libs import *
import threading

class VideoCaptureThread(threading.Thread):
    def __init__(self, src, name, index):
        super().__init__()
        self.src = src
        self.cap = cv2.VideoCapture(self.src, cv2.CAP_V4L2)
        self.name = name
        self.index = index


    def run(self):
        while True:
            ret, frame = self.cap.read()
            cv2.imshow(self.name, frame)
            cv2.moveWindow(self.name, self.index*650, 0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        VideoCaptureThread.cap.release()
        cv2.destroyAllWindows()
        

# Tạo nhiều tiến trình cho nhiều camera
cameras = ["/dev/video1", "/dev/video2"] 
names = ["Black Camera", "White Camera"]
caps = [VideoCaptureThread(cameras[i], names[i], i) for i in range(2)]
for cap in caps:
    cap.start()


