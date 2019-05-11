import numpy as np
import cv2


class PipelineRunner(object):

    def __init__(self, pipeline=None):
        self.pipeline = pipeline or []
        self.context = {}     


    def set_context(self, data):
        self.context = data


    def run(self):
        for p in self.pipeline:
            self.context = p(self.context)

        return self.context
        

class CapacityCounter():

    def __init__(self, area_mask):
        super(CapacityCounter, self).__init__()
    
        self.area_mask = area_mask
        self.all = np.count_nonzero(area_mask)
        

    def calculate_capacity(self, frame, frame_number):
        base_frame = frame

        ''' CLAHE (Contrast Limited Adaptive Histogram Equalization)
            this used for noise reduction at night time '''
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(frame)
    
        edges = cv2.Canny(frame,50,70)
        edges = ~edges
        blur = cv2.bilateralFilter(cv2.blur(edges,(21,21), 100),9,200,200)
        _, threshold = cv2.threshold(blur,230, 255,cv2.THRESH_BINARY)
        
        t = cv2.bitwise_and(threshold,threshold,mask = self.area_mask)
        
        free = np.count_nonzero(t)
        capacity = 1 - float(free)/self.all
            
        return capacity
        

    def __call__(self, context):
        frame = context['frame'].copy()
        frame_number = context['frame_number']
        
        capacity = self.calculate_capacity(frame, frame_number)
        context['capacity'] = capacity

        return context