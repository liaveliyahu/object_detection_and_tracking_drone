import numpy as np
import tellopy
import time
import cv2
import av

class Drone:
    def __init__(self, simulated=False, prints=True, speed = 100):
        self.simulated = simulated
        self.prints = prints
        self.speed = speed

        if self.prints:
            print('Creating Drone object')

        if not self.simulated:
            self.drone = tellopy.Tello()
        self.connect_to_drone()
        self.open_stream()

        self.udp_addr = 'udp://0.0.0.0:11111'

    def connect_to_drone(self):
        if self.prints:
            print('Connecting to drone')
        if not self.simulated:
            self.drone.connect()
            self.drone.wait_for_connection(60)
        if self.prints:
            print('Connection established')
    
    def open_stream(self):
        if self.simulated:
            self.vid = cv2.VideoCapture(0)
        else:
            self.drone.sock.sendto('command'.encode (' utf-8 '), self.drone.tello_addr)
            self.drone.sock.sendto('streamon'.encode (' utf-8 '), self.drone.tello_addr)

    def get_frame_dim(self):
        if self.simulated:
            w = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            return (int(w), int(h))
        else:
            w = 640
            h = 480
            return (int(w), int(h))

    def get_udp_addr(self):
        if self.simulated:
            return 0
        else:
            return self.udp_addr
        
    def quit(self):
        if self.simulated:
            self.vid.release()
            cv2.destroyAllWindows()
        else:
            self.drone.sock.sendto('streamon'.encode (' utf-8 '), self.drone.tello_addr)
            self.drone.quit()

    def takeoff(self):
        if self.prints:
            print('Taking Off')
        if not self.simulated:
            self.drone.takeoff()

    def land(self):
        if self.prints:
            print('Landing')
        if not self.simulated:
            self.drone.land()

    def move_up(self):
        if self.prints:
            print('Moving Up')
        if not self.simulated:
            self.drone.up(self.speed)

    def move_down(self):
        if self.prints:
            print('Moving Down')
        if not self.simulated:
            self.drone.down(self.speed)
    
    def move_forward(self):
        if self.prints:
            print('Moving Forward')
        if not self.simulated:
            self.drone.forward(self.speed)

    def move_backward(self):
        if self.prints:
            print('Moving Backward')
        if not self.simulated:
            self.drone.backward(self.speed)

    def move_left(self):
        if self.prints:
            print('Moving Left')
        if not self.simulated:
            self.drone.left(self.speed)

    def move_right(self):
        if self.prints:
            print('Moving Right')
        if not self.simulated:
            self.drone.right(self.speed)
    
    def move_clockwise(self):
        if self.prints:
            print('Moving Clockwise')
        if not self.simulated:
            self.drone.clockwise(self.speed)
    
    def move_counter_clockwise(self):
        if self.prints:
            print('Moving Counter Clockwise')
        if not self.simulated:
            self.drone.counter_clockwise(self.speed)

    def drone_locked(self):
        if self.prints:
            print('Object locked in the middle')

    def get_image(self):
        if self.simulated:
            ret, frame = self.vid.read()
            return frame

        else:
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
                #cv2.imshow('',image)
                #cv2.waitKey(1)
                #if frame.time_base < 1.0/60:
                #    time_base = 1.0/60
                #else:
                #   time_base = frame.time_base
                #frame_skip = int((time.time() - start_time)/time_base)


if __name__ == '__main__':
    drone = Drone()
    img = drone.get_image()

    cv2.cv2.imshow('DroneStreaming',img)
    cv2.waitKey(20000) # get 20 seconds of video

    cv2.destroyAllWindows()
