from libs import *

# Real Camera
camera_id = "/dev/video1"
videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
# Zoom Camera
camID = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=21/1 ! nvvidconv flip-method='+'2'+' ! video/x-raw, width='+'640'+', height='+'480'+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink' 
cam = cv2.VideoCapture(camID)
# Wait a second to let the port initialize
time.sleep(1)

class myThread(threading.Thread):
    numClass = 2     #The numbers of classes
    cls_dict = get_cls_dict(numClass)
    vis = BBoxVisualization(cls_dict)
    trt_yolo = TrtYOLO('obj', numClass, False)

    def __init__(self, threadID, name, paraSource):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.source = paraSource
        self.frame = None
    
    def run(self):
        global videoCapture, cam
        while True:
            getFrame(self.name, self.source)
            cv2.moveWindow(self.name, 650*self.threadID, 0)
            if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
                videoCapture.release()
                cam.release()
                cv2.destroyAllWindows()
                break
    
def getFrame(nameCam=str, para_source=None):
    # The method for using OpenCV grab() - retrieve()
    # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
    # capture.grab()
    # ret, frame = capture.retrieve()
    para_source.grab()

    ret, frame = para_source.retrieve()
    #===Detect The Fire===
    detectObjects(MultiCamera.trt_yolo, MultiCamera.vis, frame)

    if not ret:
        print("empty frame")
        return
    self.frame = frame
    cv2.imshow(nameCam, self.frame)

def detectObjects(trt_yolo, vis, frame):   
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

#Create new threads
thread1 = myThread(0, "realCam", videoCapture)
thread2 = myThread(1, "zoomCam", cam)
#Start new Threads
thread1.start()
thread2.start()
    