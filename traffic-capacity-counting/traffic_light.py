import random
import time

# from traffic_capacity import mymain
# mymain()

#function to calculate sum of timer for all lanes
def returnSum(timer):  
     sum = 0
     for i in timer: 
           sum = sum + timer[i] 
     return sum

while True:
    capacity = []
    timer = {}
    number_of_lanes = random.randint(3,4) #considering scenario of 3 to 4 lanes

    #taking random capacity values for execution purpose 
    for j in range(number_of_lanes):
        capacity.append(round(random.uniform(2.00,50.99),5))

    # capacity.sort()

    for i in capacity:
        if((int(i)*2) < 30):
            timer[capacity[capacity.index(i)]] = 30 #min time for a lane in 30seconds
        elif((int(i)*2) > 60):
            timer[capacity[capacity.index(i)]] = 60 #max time for a lane in 60seconds
        else:
            timer[capacity[capacity.index(i)]] = int(i)*2

    sum = returnSum(timer) #calculating total sum of timer for all lanes

    print("\n[Number of Lanes] => ",number_of_lanes,"\n[Capacity : Timer] => ",timer, "\n[Cycle time] => ",sum,"seconds")
    
    time.sleep(sum) #wait till a cycle in completed

