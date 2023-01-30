from libs import *

# Real Camera
camera_id = "/dev/video1"
videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
# Zoom Camera
camID = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=21/1 ! nvvidconv flip-method='+'2'+' ! video/x-raw, width='+'640'+', height='+'480'+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink' 
cam = cv2.VideoCapture(camID)
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

#ádjkhbạkdbalksdblábdá
realCam = MultiCamera(videoCapture)
zoomCam = MultiCamera(cam)
while True:

    realCam.getFrame(realCam.source)
    cv2.imshow("realCam", realCam.frame)
    cv2.moveWindow("realCam", 0, 0)

    zoomCam.getFrame(zoomCam.source)
    cv2.imshow("zoomCam", zoomCam.frame)
    cv2.moveWindow("zoomCam", 650, 0)

    if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
        break

# photo = None
# def updateFrame():
#     global canvas, photo, frame, canvas2, frame2, photo2

#     # The method for using OpenCV grab() - retrieve()
#     # We are not using read() here because, documentation insists that it is slower in multi-thread environment.
#     # capture.grab()
#     # ret, frame = capture.retrieve()
#     # link: https://www.youtube.com/watch?v=XEvpWg8msLg
    
#     videoCapture.grab()
#     cam.grab()
#     ret, frame = videoCapture.retrieve()
#     ret, frame2 = cam.retrieve()

#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

#     canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

#     frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
#     photo2 = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame2))

#     canvas2.create_image(0, 0, image=photo2, anchor=tkinter.NW)
#     window.after(10, updateFrame)


# window = Tk()

# window.title("The Fire Detection")
# window.geometry("1300x650")
# # window.resizable(False, False)
# #add background
# canvas1 = Canvas(window, width=1120, height=800, bg='red')
# canvas1.place(x = 0, y = 0) 

# #add cam
# canvas = Canvas(window, width=640, height=480)
# canvas.place(x = 4, y = 100)
# canvas2 = Canvas(window, width=640, height=480)
# canvas2.place(x = 650, y = 100)
# updateFrame()

# window.mainloop()
