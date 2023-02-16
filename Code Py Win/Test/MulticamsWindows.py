from libs import *

# Real Camera
camera_id = "/dev/video1"
videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)

class MultiCamera:
    def __init__(self, para_source) -> None:
        self.source = para_source
        self.frame = None
    
    def getFrame(self, nameCam=str):
        # The method for using OpenCV grab() - retrieve()
        # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
        # capture.grab()
        # ret, frame = capture.retrieve()
        para_source = self.source
        para_source.grab()

        ret, frame = para_source.retrieve()
        #===Detect The Fire===
        # self.detectObjects(MultiCamera.trt_yolo, MultiCamera.vis, frame)

        if not ret:
            print("empty frame")
            return
        self.frame = frame
        cv2.imshow(nameCam, self.frame)

    
# 2 object in class MultiCamera
realCam = MultiCamera(videoCapture)
while True:
    realCam.getFrame("realCam")
    cv2.moveWindow("realCam", 0, 0)

    print("oke")
    
    if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
        break
    
videoCapture.release()
cv2.destroyAllWindows()
