from libs import *
import datetime

# Class Camera
numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj_test', numClass, False)

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
        return frame

if __name__ == "__main__":
    image = cv2.imread("/home/khanh/LuanVan/Test/FileTest/img1.jpg")

    frame = detectObjects(image)

    cv2.imshow("Ảnh gốc", frame)
    cv2.resizeWindow("Ảnh gốc", 640, 480)

    cv2.waitKey(0)

    cv2.destroyAllWindows()
