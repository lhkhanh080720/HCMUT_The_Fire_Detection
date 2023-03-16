from datetime import datetime
# nameVideo = 'Video/' + str(time.tm_year) + '.mp4'
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
dt_string = dt_string.replace('/', '-')
dt_string = dt_string.replace(' ', '_')
dt_string = dt_string.replace(':', '-')
print("date and time =", dt_string)








# import os
# import time
# import argparse # Library support Command Line Interface (CLI)
# import numpy as np

# import cv2
# import pycuda.autoinit  # This is needed for initializing CUDA driver

# from utils.yolo_classes import get_cls_dict
# from utils.camera import add_camera_args, Camera
# from utils.display import open_window, set_display, show_fps
# from utils.visualization import BBoxVisualization
# from utils.yolo_with_plugins import TrtYOLO

# #print(cv2.__version__)

# # =========Take the video and process:=========
# # cam = cv2.VideoCapture('Video/myCam.avi')
# # in while:
# #     ret, frame = cam.read()

# #     cv2.imshow('realVideo', frame)
# #     cv2.moveWindow('realVideo', 0, 0)    
# # =============================================

# # =========Save the Video:=========
# # outVid = cv2.VideoWriter('Video/myCam.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (dispW, dispH)) # Write the Video with fps = 21
# # in while:
# #     ret, frame = cam.read()

# #     cv2.imshow('realVideo', frame)
# #     cv2.moveWindow('realVideo', 0, 0)  
# #     outVid.write(frame)  
# # outVid.release()       #Make sure Write the video is turn off
# # =============================================
# def detectObjects(trt_yolo, vis, frame):   
#     boxes, confs, clss = trt_yolo.detect(frame, 0.3)

#     #Precise poison filter (> 0.6)
#     indexDel = []
#     for index, value in enumerate(confs):
#         if value <= 0.7:
#             indexDel.append(index)
#     boxes = np.delete(boxes, indexDel, 0)
#     confs = np.delete(confs, indexDel)
#     clss = np.delete(clss, indexDel)
    
#     if len(confs) > 0: 
#         frame, (x_min, y_min, x_max, y_max) = vis.draw_bboxes(frame, boxes, confs, clss)
#         flagC = 1

    
# windowTitle = 'USB Cam'
# def showCam():
#     outVid = cv2.VideoWriter('Video/Video1_detect.avi', cv2.VideoWriter_fourcc(*'XVID'), 21, (640, 480)) # Write the Video with fps = 21

#     numClass = 2     #The numbers of classes
#     cls_dict = get_cls_dict(numClass)
#     vis = BBoxVisualization(cls_dict)
#     trt_yolo = TrtYOLO('obj', numClass, False)

#     camera_id = "/dev/video0"
#     videoCapture = cv2.VideoCapture('Video2.mp4')
#     videoCapture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
#     fps = 0
#     if videoCapture.isOpened():
#         windowHandle = cv2.namedWindow(windowTitle, cv2.WINDOW_AUTOSIZE)
#         preTime = time.time()
#         while True:
#             ret, frame = videoCapture.read()

#             # #Calc FPS
#             Time = time.time()
#             curr_fps = 1.0 / (Time - preTime)
#             fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
#             preTime = Time

#             if cv2.getWindowProperty(windowTitle, cv2.WND_PROP_AUTOSIZE) >= 0:
#                 cv2.putText(frame, f"FPS: {int(fps)}", (10, 25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0,0,0), 3)
#                 detectObjects(trt_yolo, vis, frame)
#                 cv2.imshow(windowTitle, frame)
#                 cv2.moveWindow(windowTitle, 0, 0)
#                 outVid.write(frame) 
#             else:
#                 break
#             if cv2.waitKey(1) == ord('q'): #check Button 'q' in 1 milis and do st...
#                 break
#         videoCapture.release()
#         cv2.destroyAllWindows()
#         outVid.release()    
#     else:
#         print('Unable to open Camera!')


# if __name__ == '__main__':
#     showCam()

