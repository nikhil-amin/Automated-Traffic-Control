import random
import time
import threading

MIN_LANE_TIME = 15  #min time for a lane in 15 seconds
MAX_LANE_TIME = 60  #max time for a lane in 60 seconds

#function to calculate sum of timer for all lanes
def returnSum(timer):
    sum = 0
    for i in timer: 
          sum = sum + timer[i] 
    return sum

def mymain2(in_q, dict_out_q):
    while True:
        capacity = []
        receivedCapacity = in_q.get()
        print("receivedCapacity: " ,receivedCapacity)

        capacity.append(receivedCapacity)
        timer = {}
        number_of_lanes = random.randint(2,2) + 2 #considering scenario of 4 lanes
        
        #taking random capacity values for execution purpose 
        for j in range(number_of_lanes):
            capacity.append(round(random.uniform(2.00,50.99),5))

        for i in capacity:
            if((int(i)*2) < 30):
                timer[capacity[capacity.index(i)]] = MIN_LANE_TIME 
            elif((int(i)*2) > 60):
                timer[capacity[capacity.index(i)]] = MAX_LANE_TIME 
            else:
                timer[capacity[capacity.index(i)]] = int(i)*2
        
        sum = returnSum(timer) #calculating total sum of timer for all lanes
        dict_out_q.put(timer)
        
        print("[Number of Lanes] => ",number_of_lanes,"\n[Capacity : Timer] => ",timer, "\n[Cycle time] => ",sum,"seconds")
        
        in_q.task_done()
        
        time.sleep(sum) #wait till a cycle in completed