import random
import time
from traffic_capacity import mymain1
import threading

from flask import Flask
app = Flask(__name__)

# from traffic_capacity import mymain
# mymain()

#function to calculate sum of timer for all lanes

def returnSum(timer):
    sum = 0
    for i in timer: 
          sum = sum + timer[i] 
    return sum

@app.route('/')
def mymain2(in_q):
    while True:
        capacity = []
        receivedCapacity = in_q.get()
        print("receivedCapacity: " ,receivedCapacity)

        # receivedCapacity = mymain1()
        capacity.append(receivedCapacity)
        timer = {}
        number_of_lanes = random.randint(2,3) + 1 #considering scenario of 3 to 4 lanes
        #taking random capacity values for execution purpose 
        for j in range(number_of_lanes):
            capacity.append(round(random.uniform(2.00,50.99),5))
        # capacity.sort()
        for i in capacity:
            if((int(i)*2) < 30):
                timer[capacity[capacity.index(i)]] = 3 #min time for a lane in 30seconds
            elif((int(i)*2) > 60):
                timer[capacity[capacity.index(i)]] = 6 #max time for a lane in 60seconds
            else:
                timer[capacity[capacity.index(i)]] = 1 #int(i)*2
        sum = returnSum(timer) #calculating total sum of timer for all lanes

        print("[Number of Lanes] => ",number_of_lanes,"\n[Capacity : Timer] => ",timer, "\n[Cycle time] => ",sum,"seconds")
        in_q.task_done()
        # return str(sum)
        time.sleep(sum) #wait till a cycle in completed

# if __name__ == "__main__":
#     t1 = threading.Thread(target=mymain1)
#     t2 = threading.Thread(target=mymain2)
#     t1.start()
#     t2.start()
        # mymain2()
        # print(sum)
        # time.sleep(sum)