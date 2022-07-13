import cv2
from drone.drone import Drone
from time import sleep

FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 0.5
THICKNESS = 1
BLACK = (0,0,0)
BLUE = (255,0,0)
GREEN = (0,255,0)
RED = (0,0,255)

class Brain:
    def __init__(self, object,
                 err_dist=3, err_radius=30, track_distance=150,
                 ref_object_width=315, ref_object_dist=30,
                 delay=0, prints=True, simulated=False):
        self.drone = Drone(simulated, prints)
        self.object = object

        self.track_distance = track_distance
        self.err_dist = err_dist

        self.measure_factor = self.calc_measure_factor(ref_object_width, ref_object_dist)
        self.err_radius = err_radius
        self.image_center = None

        w, h = self.drone.get_frame_dim()
        self.calc_image_center(w, h)

        self.delay = delay
        
        self.udp_addr = self.drone.get_udp_addr()
        #self.takeoff()

    def takeoff(self):
        self.drone.takeoff()

    def abort(self):
        self.drone.land()
        self.drone.quit()

    def act(self, img, object, x1, y1, x2, y2):
        if object == self.object:
            center_mass = self.calc_center_mass(x1, y1, x2, y2)

            self.object_centering(img, center_mass)

            #self.object_distancing(img, x2-x1)

    def get_image(self):
        return self.drone.get_image()

    def land(self):
        self.drone.land()

    # distance functions
    def calc_measure_factor(self, ref_object_width, ref_object_dist):
        measure_factor = ref_object_dist * ref_object_width
        return measure_factor

    def calc_distance(self, img, current_object_width):
        distance = self.measure_factor / current_object_width

        label = 'Object distance: ' + str(round(distance,2))
        cv2.line(img, (20, 17), (200, 17), BLACK, 20)
        cv2.putText(img, label, (20,20), FONT, FONT_SCALE, GREEN, THICKNESS)

        return distance

    def object_distancing(self, img, current_object_width):
        object_distance = self.calc_distance(img, current_object_width)
        
        if object_distance > self.track_distance + self.err_radius:
            self.drone.move_forward()
        elif object_distance < self.track_distance - self.err_radius:
            self.drone.move_backward()

    # 2D plain object location functions
    def calc_image_center(self, image_width, image_height):
        image_center = (image_width//2,image_height//2)
        self.image_center = image_center
        return image_center

    def calc_center_mass(self, x1, y1, x2, y2):
        object_center_mass = (x1 + x2)//2, (y1 + y2)//2
        return object_center_mass

    def object_centering(self, img, center_mass):
        self.draw_centers(img, center_mass)
        
        o_x, o_y = center_mass
        i_x, i_y = self.image_center

        center_flag = True

        if o_y < i_y - self.err_radius:
            self.drone.move_up()
            sleep(self.delay)
            self.drone.speed = 0
            self.drone.move_up()
            center_flag = False
        elif o_y > i_y + self.err_radius:
            self.drone.move_down()
            sleep(self.delay)
            self.drone.speed = 0
            self.drone.move_down()
            center_flag = False
        
        if o_x < i_x - self.err_radius:
            self.drone.move_counter_clockwise()
            sleep(self.delay)
            self.drone.speed = 0
            self.drone.move_counter_clockwise()
            center_flag = False
        elif o_x > i_x + self.err_radius:
            self.drone.move_clockwise()
            center_flag = False
            sleep(self.delay)
            self.drone.speed = 0
            self.drone.move_clockwise()
        self.drone.speed = 60
        if center_flag:
            self.drone.drone_locked()

    def draw_centers(self, img, center_mass):
        cv2.circle(img, (center_mass[0],center_mass[1]), 2, (255,0,0), 4)
        cv2.line(img, (self.image_center[0]-20, self.image_center[1]),
                (self.image_center[0]+20, self.image_center[1]), RED, 2)
        cv2.line(img, (self.image_center[0], self.image_center[1]-20),
                (self.image_center[0], self.image_center[1]+20), RED, 2)

if __name__ == '__main__':
    brain = Brain('cell phone', simulated=True)
    while True:
        img = brain.get_image()
        brain.draw_centers(img, (400,400))
        cv2.imshow('image',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    brain.abort()
