#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from apriltag_ros.msg import AprilTagDetectionArray
#from geometry_msgs import PoseWithCovariance

#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('gnd_pos_truth', String, queue_size = 30)

def callback0(data):
        
    x_pos = data.detections[0].pose.pose.pose.position.x
    y_pos = data.detections[0].pose.pose.pose.position.y
    tag_size = data.detections[0].size
    tag_id = data.detections[0].id
    print (x_pos)
    str2pub = "X: " + str(x_pos) " Y: " + str(y_pos)
    pub.publish(str2pub)
    # try:
        
    #     print("try")
    #     s=0
    #     print(s)
    #     s = data.detections.size
    #     #x_pos = data.detections[0].pose.pose.position.x
    #     #str2pub = "X: "+ x_pos
    #     #pub.publish(str2pub)
    #     print(s)
    # except:
    #     print("no tags detected")

def apriltagProcessing():
    rospy.init_node('apriltag_data_processing', anonymous=True)

    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    apriltagProcessing()