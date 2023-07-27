import rclpy
from rclpy.node import Node
import csv #For reading and writing data to csv
from std_msgs.msg import Float64
import sys
import cv2 # OpenCV library
from cv_bridge import CvBridge
from datetime import datetime
from .submodules.object_class import Object

turtlebot_name_1 = 'R2TB_O1'
turtlebot_name_2 = 'R2TB_O2'
time_stamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
path_to_photo = f'/media/external/nearest_image{time_stamp}.png'
path_to_csv = '/home/ubuntu/ros2_ws/src/green_object_finder/green_object_finder/nearby_objects.csv'

class DistanceSub(Node):
    
    def __init__(self):
        self.current_distance = 1.5
        self.tb1_distance = read_csv()
        self.tb2_distance = None
        self.counter = 1
        super().__init__('distance_sub')
        self.sub = self.create_subscription(Float64, turtlebot_name_2, self.subscriber_callback, 10)

    def subscriber_callback(self, msg: Float64):
        self.tb2_distance = msg.data
        
        if self.tb1_distance < self.tb2_distance:
            print(f'turtlebot {turtlebot_name_1} is closer') 
        
        elif self.tb2_distance < self.tb1_distance:
            print(f'turtlebot {turtlebot_name_2} is closer') 

        elif self.tb1_distance == self.tb2_distance:
            print('they are equal')

        else:
            print('there was an error')



        if self.counter == 1:
            sys.exit()
        else:
            self.counter += 1

    def take_photo(self):
        """This function is called once the turtlebot has found the closest green object. It will take
        a photo and save it as a png named 'nearest_image' followed by a time stamp.
        """
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(path_to_photo, frame)
            print("Photo Taken")

def read_csv():
    """This function will read the csv generated by closest_objects.py and add them to a list to be
    iterated over.

    Returns:
        list: Returns a list of objects of the object class.
    """
    obj_distance = None
    with open(path_to_csv, 'r') as f:
        reader = csv.reader(f)

        for lines in reader:
            obj_distance = float(lines[2])

    return obj_distance


def main():
    rclpy.init(args=None)
    my_node = DistanceSub()
    rclpy.spin(my_node)
    my_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()