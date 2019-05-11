from traffic_capacity import traffic_capacity
from traffic_light import traffic_light
from GUI import GUI

import threading
import queue


if __name__ == "__main__":

    number_of_lanes = (int(input("Enter number of lanes for simulations: ")))

    q_capacity = queue.LifoQueue()
    q_timer = queue.LifoQueue()
    q_number_of_lanes = queue.LifoQueue()
    q_camera_frames = queue.Queue()

    q_number_of_lanes.put(number_of_lanes)

    # 3 programs are run parallel using threads
    t1 = threading.Thread(target=traffic_capacity,args=(q_capacity,q_camera_frames))  # Reading & calculation of capacity from camera feed
    t2 = threading.Thread(target=traffic_light,args=(q_capacity,q_timer,q_number_of_lanes))  # Assigning timers for lane based on capacity
    t3 = threading.Thread(target=GUI,args=(q_timer,q_number_of_lanes,q_camera_frames))  # GUI display
    
    t1.start()  # Start thread1 
    t2.start()  # Start thread2
    t3.start()  # Start thread3

    t1.join()  # Wait till thread1 is complete
    t2.join()  # Wait till thread2 is complete
    t3.join()  # Wait till thread3 is complete

    print("All the threads are terminated!")