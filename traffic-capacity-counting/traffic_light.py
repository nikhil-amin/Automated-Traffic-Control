import random
import time
import threading

MIN_LANE_TIME = 15  # min time for a lane in 15 seconds
MAX_LANE_TIME = 60  # max time for a lane in 60 seconds


# function to calculate sum of timer for all lanes
def returnSum(timer):
    
    cycleTime = 0
    for i in timer: 
          cycleTime = cycleTime + timer[i] 
    return cycleTime


def traffic_light(q_capacity, q_timer, q_number_of_lanes):

    number_of_lanes = q_number_of_lanes.get()  # considering scenario of 4 lanes
    while True:
        capacity = []
        receivedCapacity = q_capacity.get()  # taking capacity from queue
        print("[Received Capacity] =>" ,receivedCapacity)

        capacity.append(receivedCapacity)
        timer = {}
        
        
        # taking random capacity values for execution purpose 
        for j in range(number_of_lanes-1):
            capacity.append(round(random.uniform(2.00,50.99),5))

        for i in capacity:
            if((int(i)*2) < 30):
                timer[capacity[capacity.index(i)]] = MIN_LANE_TIME 
            elif((int(i)*2) > 60):
                timer[capacity[capacity.index(i)]] = MAX_LANE_TIME 
            else:
                timer[capacity[capacity.index(i)]] = int(i)*2
        
        cycleTime = returnSum(timer)  # calculating total sum of timer for all lanes
        q_timer.put(timer)  # putting timer dictionary on a queue
        q_number_of_lanes.put(number_of_lanes)
        print("[Number of Lanes] => ",number_of_lanes,"\n[Capacity : Timer] => ",timer, "\n[Cycle time] => ",cycleTime,"seconds")
        
        q_capacity.task_done()
        
        time.sleep(cycleTime)  # wait till a cycle in completed
