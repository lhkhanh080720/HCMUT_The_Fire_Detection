from libs import *
import threading
import multiprocessing

lock = threading.Lock()

# Real Camera
camera_id = "/dev/video1"
videoCapture = cv2.VideoCapture(camera_id, cv2.CAP_V4L2)
# Zoom Camera
camID = "/dev/video2"
cam = cv2.VideoCapture(camID)
# Wait a second to let the port initialize
numClass = 2     #The numbers of classes
cls_dict = get_cls_dict(numClass)
vis = BBoxVisualization(cls_dict)
trt_yolo = TrtYOLO('obj', numClass, False)
time.sleep(1)

def get_frame(cap, pipe):
    global trt_yolo, vis, lock
    while True:
        print("Start loop1")
        ret, frame = cap.read()
        frame = detect_objects(trt_yolo, vis, frame)
        print("==> end")
        if not ret:
            print("Empty Frame!")
            break
        pipe.send(frame)
    cap.release()

def display_frame(pipe, window_name, index):
    while True:
        frame = pipe.recv()
        cv2.imshow(window_name, frame)
        cv2.moveWindow(window_name, index*650, 0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def detect_objects(trt_yolo, vis, frame):
    print("===> start Lock")
    global lock
    with lock:    
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
        print("End Lock")
        return frame

if __name__ == '__main__':
    camera_ids = [cam, videoCapture]
    window_names = ['Zoom Cam', 'Real Cam']
    window_index = [0, 650]
    
    pipes = [multiprocessing.Pipe() for _ in range(2)]
    gets = [multiprocessing.Process(target=get_frame, args=(camera_ids[i], pipes[i][0],)) for i in range(1)]
    [process.start() for process in gets]

    display_processes = [multiprocessing.Process(target=display_frame, args=(pipes[i][1], window_names[i], i, )) for i in range(1)]
    [process.start() for process in display_processes]

    [process.join() for process in gets + display_processes]