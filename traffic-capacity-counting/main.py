from traffic_capacity import mymain1
from traffic_light import mymain2
from GUI import mymain3

import threading
import queue


if __name__ == "__main__":

    q = queue.LifoQueue()
    dict_q = queue.LifoQueue()

    # 3 programs are run parallel using threads
    t1 = threading.Thread(target=mymain1,args=(q,))  # Reading & calculation of capacity from camera feed
    t2 = threading.Thread(target=mymain2,args=(q,dict_q))  # Assigning timers for lane based on capacity
    t3 = threading.Thread(target=mymain3,args=(q,dict_q))  # GUI display
    
    t1.start()  # Start thread1 
    t2.start()  # Start thread2
    t3.start()  # Start thread3

    t1.join()  # Wait till thread1 is complete
    t2.join()  # Wait till thread2 is complete
    t3.join()  # Wait till thread3 is complete

    print("All the threads are terminated!")