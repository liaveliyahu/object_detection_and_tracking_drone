# object_detection_and_tracking_drone
An autonomous drone that detects and tracks an object

## Issues
* Get video from Tello drone - I had some difficulties  to get the video from the drone. the problem caused by the Firewall. When I moved to another PC without the Firewall I amanged to get video data from the drone.
* Sync video - when I used YoloV5 to preprocess each frame I got from the drone I got Increased delay that makes the program impossible to work with. at the beggning it took 3 seconds between each frames to preprocess and after each fram it got worse by around 1 second. The solution was to remove "time.sleep(FPS)" from the YoloV5 code. It created too much Idle time of the program.
* Improve drone action time by using Pygame - need to add it to the code.
