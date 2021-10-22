import numpy as np
import tellopy
import time
import cv2
import av

class Drone:
    def __init__(self, speed = 30):
        print('Drone object created')
        self.drone = tellopy.Tello()
        self.connect_to_drone()
        self.speed = speed

    def connect_to_drone(self):
        print('Connecting to drone')
        self.drone.connect()
        self.drone.wait_for_connection(60)
        print('Connection established')
    
    def quit(self):
        self.drone.quit()

    def takeoff(self):
        print('Taking Off')
        #self.drone.takeoff()

    def land(self):
        print('Landing')
        #self.drone.land()

    def move_up(self):
        print('Moving Up')
        #self.drone.up(self.speed)

    def move_down(self):
        print('Moving Down')
        #self.drone.down(self.speed)
    
    def move_forward(self):
        print('Moving Forward')
        #self.drone.forward(self.speed)

    def move_backward(self):
        print('Moving Backward')
        #self.drone.backward(self.speed)

    def move_left(self):
        print('Moving Left')
        #self.drone.left(self.speed)

    def move_right(self):
        print('Moving Right')
        #self.drone.right(self.speed)
    
    def move_clockwise(self):
        print('Moving Clockwise')
        #self.drone.clockwise(self.speed)
    
    def move_counter_clockwise(self):
        print('Moving Counter Clockwise')
        #self.drone.counter_clockwise(self.speed)

    def drone_locked(self):
        print('Object locked in the middle')

    def get_image(self):
        retry = 3
        container = None
        while container is None and 0 < retry:
            retry -= 1
            try:
                container = av.open(self.drone.get_video_stream())
            except av.AVError as ave:
                print(ave)
                print('retry...')
        
        frame_skip = 300
        for frame in container.decode(video=0):
            if 0 < frame_skip:
                frame_skip -= 1
                continue
            start_time = time.time()
            image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
            return image
            cv2.imshow('',image)
            cv2.waitKey(1)
            #if frame.time_base < 1.0/60:
            #    time_base = 1.0/60
            #else:
            #   time_base = frame.time_base
            #frame_skip = int((time.time() - start_time)/time_base)
