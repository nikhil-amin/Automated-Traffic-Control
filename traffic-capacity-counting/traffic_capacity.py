import logging
import logging.handlers
import os
import time
import sys
import _thread

import cv2
import numpy as np
import skvideo.io
import utils
import matplotlib.pyplot as plt

import datetime

# without this some strange errors happen
cv2.ocl.setUseOpenCL(False)

# ============================================================================

IMAGE_DIR = "./out"
VIDEO_SOURCE = './input.mp4'
SHAPE = (480, 640)
AREA_PTS = np.array([[390, 416], [343, 73], [441, 83], [640, 336], [640, 420]]) 

from pipeline import (
    PipelineRunner,
    CapacityCounter,
    # ContextCsvWriter
)
# ============================================================================


def mymain():
    log = logging.getLogger("main")

    base = np.zeros(SHAPE + (3,), dtype='uint8')
    area_mask = cv2.fillPoly(base, [AREA_PTS], (255, 255, 255))[:, :, 0]

    pipeline = PipelineRunner(pipeline=[
        CapacityCounter(area_mask=area_mask, save_image=True, image_dir=IMAGE_DIR),
        # saving every 10 seconds
        #ContextCsvWriter('./report.csv', start_time=1505494325, fps=1, faster=10, field_names=['capacity'])
    ], log_level=logging.DEBUG)

    # Set up image source
    # cap = skvideo.io.vreader(VIDEO_SOURCE)
    cap = cv2.VideoCapture(0)

    frame_number = -1
    st = time.time()
    
    try:
        while(True):
            # print(cap.read())
            frame_number += 1
            flag, frame = cap.read()
            # print("flag", flag)
            # print("frame", frame)
            pipeline.set_context({
                'frame': frame,
                'frame_number': frame_number,
            })
            context = pipeline.run()

            print("[{}] \t Frame: {} \t Capacity: {}%".format(datetime.datetime.now().strftime('%d-%m-%Y %I:%M:%S %p'),context['frame_number'],round(context['capacity']*100,5)))
            
            #_thread.start_new_thread(pipeline.run, ())
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
        cap.release()
        # for frame in cap:
            # if not frame.any():
                # log.error("Frame capture failed, skipping...")
# 
            # frame_number += 1
# 
            # pipeline.set_context({
                # 'frame': frame,
                # 'frame_number': frame_number,
            # })
            # pipeline.run()
# 
            # skipping 10 seconds
            # for i in range(240):
                # cap.__next__()
        
    except Exception as e:
        log.exception(e)
# ============================================================================

if __name__ == "__main__":
    # log = utils.init_logging()

    # if not os.path.exists(IMAGE_DIR):
    #     log.debug("Creating image directory `%s`...", IMAGE_DIR)
    #     os.makedirs(IMAGE_DIR)

    mymain()
