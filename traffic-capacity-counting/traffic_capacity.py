import datetime
import cv2
import numpy as np

cv2.ocl.setUseOpenCL(False)

SHAPE = (480, 640)
AREA_PTS = np.array([[390, 416], [343, 73], [441, 83], [640, 336], [640, 420]]) 

from pipeline import (
    PipelineRunner,
    CapacityCounter
)


def traffic_capacity(q_capacity,q_camera_frames):

    base = np.zeros(SHAPE + (3,), dtype='uint8')
    area_mask = cv2.fillPoly(base, [AREA_PTS], (255, 255, 255))[:, :, 0]

    pipeline = PipelineRunner(pipeline=[
        CapacityCounter(area_mask=area_mask)
    ])

    cap = cv2.VideoCapture(0)  # Taking camera input
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cap.set(cv2.CAP_PROP_FPS, 24)

    frame_number = -1
    
    try:
        while(True):
            frame_number += 1
            flag, frame = cap.read()
            
            pipeline.set_context({
                'frame': frame,
                'frame_number': frame_number,
            })            
            context = pipeline.run()

            img = {}
            img["frame"] = frame
            q_camera_frames.put(img)

            print("\n[{}] \t Frame: {} \t Capacity: {}%".format(datetime.datetime.now().strftime('%d-%m-%Y %I:%M:%S %p'),context['frame_number'],round(context['capacity']*100,5)))
            q_capacity.put(round(context['capacity']*100,5))  # putting capacity on a queue

        cap.release()
        
    except Exception as e:
        print("EXCEPTION: ",e)