import cv2
import multiprocessing

# Real Camera
camera_id1 = "/dev/video1"
videoCapture1 = cv2.VideoCapture(camera_id1, cv2.CAP_V4L2)
# Zoom Camera
camera_id2 = "/dev/video1"
videoCapture2 = cv2.VideoCapture(camera_id2, cv2.CAP_V4L2)
# Wait a second to let the port initialize
time.sleep(1)

def process_frame(cap, pipe):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        pipe.send(frame)
    cap.release()

def display_frames(pipe, window_name):
    while True:
        frame = pipe.recv()
        cv2.imshow(window_name, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    camera_ids = [videoCapture1, videoCapture2]
    window_names = ['Camera 0', 'Camera 1']

    pipes = [multiprocessing.Pipe() for _ in range(2)]
    processes = [multiprocessing.Process(target=process_frame, args=(camera_ids[i], pipes[i][0],)) for i in range(2)]
    [process.start() for process in processes]

    display_processes = [multiprocessing.Process(target=display_frames, args=(pipes[i][1], window_names[i],)) for i in range(2)]
    [process.start() for process in display_processes]

    [process.join() for process in processes + display_processes]
