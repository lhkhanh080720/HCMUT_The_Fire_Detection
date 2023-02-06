from libs import *
import datetime

# Real Camera
camera_id = "/dev/video0"
videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
# Zoom Camera
camera_id2 = "/dev/video1"
cam = cv2.VideoCapture(camera_id2, cv2.CAP_V4L2)
# Wait a second to let the port initialize
time.sleep(1)

class MultiCamera:
    numClass = 2     #The numbers of classes
    cls_dict = get_cls_dict(numClass)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO('obj', numClass, False)

    def __init__(self, para_source) -> None:
        self.source = para_source
        self.frame = None
    
    def getFrame(self, capture):
        # The method for using OpenCV grab() - retrieve()
        # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
        # capture.grab()
        # ret, frame = capture.retrieve()
        capture.grab()

        ret, frame = capture.retrieve()
        #===Detect The Fire===
        self.detectObjects(MultiCamera.trt_yolo, MultiCamera.vis, frame)

        if not ret:
            print("empty frame")
            return
        self.frame = frame

    def detectObjects(self, trt_yolo, vis, frame):   
        boxes, confs, clss = trt_yolo.detect(frame, 0.3)

        #Precise poison filter (> 0.6)
        indexDel = []
        for index, value in enumerate(confs):
            if value <= 0.7:
                indexDel.append(index)
        boxes = np.delete(boxes, indexDel, 0)
        confs = np.delete(confs, indexDel)
        clss = np.delete(clss, indexDel)
        
        if len(confs) > 0: 
            self.frame, (x_min, y_min, x_max, y_max) = vis.draw_bboxes(frame, boxes, confs, clss)

realCam = MultiCamera(videoCapture)
zoomCam = MultiCamera(cam)

count = time.time()
while True:
    if time.time() - count >= 20:
        count = time.time()
        current_time = datetime.datetime.now().time()
        print("===========================")
        print("TIME = " + str(current_time.strftime("%H:%M:%S")))
        with open("/sys/devices/virtual/thermal/thermal_zone1/temp", "r") as temp_file:
            print("CPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone2/temp", "r") as temp_file:
            print("GPU: " + str(int(temp_file.read().strip())/1000))
        with open("/sys/devices/virtual/thermal/thermal_zone5/temp", "r") as temp_file:
            print("Thermal Fan: " + str(int(temp_file.read().strip())/1000))

    realCam.getFrame(realCam.source)
    cv2.imshow("Black Cam", realCam.frame)
    cv2.moveWindow("Black Cam", 0, 0)

    zoomCam.getFrame(zoomCam.source)
    cv2.imshow("White Cam", zoomCam.frame)
    cv2.moveWindow("White Cam", 650, 0)



    if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
        break
            