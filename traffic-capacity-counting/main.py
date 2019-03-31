from traffic_capacity import mymain1
from traffic_light import mymain2

import threading
import queue
if __name__ == "__main__":
    q = queue.LifoQueue()

    t1 = threading.Thread(target=mymain1,args=(q,))
    t2 = threading.Thread(target=mymain2,args=(q,))
    
    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All the threads are terminated!")