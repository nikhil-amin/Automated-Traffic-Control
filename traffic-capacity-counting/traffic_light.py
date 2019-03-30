import random
import time

def returnSum(timer): 
      
     sum = 0
     for i in timer: 
           sum = sum + timer[i] 
       
     return sum

while True:
    capacity = []
    timer = {}
    for j in range(4):
        capacity.append(round(random.uniform(2.00,50.99),5))
    # capacity.sort()

    for i in capacity:
        if((int(i)*2) < 30):
            timer[capacity[capacity.index(i)]] = 30 #min time for a lane in 30seconds
        elif((int(i)*2) > 60):
            timer[capacity[capacity.index(i)]] = 60 #max time for a lane in 60seconds
        else:
            timer[capacity[capacity.index(i)]] = int(i)*2

    sum = returnSum(timer)

    print("\n[Capacity : Timer] => ",timer, "\n[Cycle time] => ",sum,"seconds")
    
    time.sleep(sum) #wait till a cycle in completed

