from libs import *
import datetime

# Class Camera
numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj', numClass, False)

def detectObjects(frame):  
    global vis, trt_yolo
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
        frame, (x_min, y_min, x_max, y_max) = vis.draw_bboxes(frame, boxes, confs, clss)

if __name__ == "__main__":

    cam = cv2.VideoCapture('video1.avi')

    while True: 
        ret, frame = cam.read()
        print(frame)
        detectObjects(frame)
        cv2.imshow('Result', frame)
        cv2.resizeWindow('Result', 1280, 720)
        cv2.moveWindow('Result', 0, 0)   
        cv2.waitKey(1)
