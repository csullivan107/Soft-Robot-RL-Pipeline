#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from apriltag_ros.msg import AprilTagDetectionArray
from soft_robot_learning.msg import apriltag_data
import numpy as np
import quaternion
#from geometry_msgs import PoseWithCovariance

#these values will be used to 0 out each episode
x_calib_zero = 0
y_calib_zero = 0

# def calculateVector(xP,yP,zP,xO,yO,zO,wO):


#define publisher
#message format - "x: num y: num"
pub = rospy.Publisher('/gnd_pos_truth', apriltag_data, queue_size = 30)


def callback0(data):

    len = .020 #20 mm in meter representation

    x_pos = data.detections[0].pose.pose.pose.position.x
    y_pos = data.detections[0].pose.pose.pose.position.y
    z_pos = data.detections[0].pose.pose.pose.position.z
    #quaternian orientation
    x_quat = data.detections[0].pose.pose.pose.orientation.x
    y_quat = data.detections[0].pose.pose.pose.orientation.y
    z_quat = data.detections[0].pose.pose.pose.orientation.z
    w_quat = data.detections[0].pose.pose.pose.orientation.w

    # tag_quat = np.quaternian(w_quat,x_quat,y_quat,z_quat)
    # rot_mat = np.quaternian.as_rotation_matrix(tag_quat)
    

    tag_size = data.detections[0].size
    tag_id = data.detections[0].id
    message = apriltag_data()
    message.x_pos_gnd = x_pos
    message.y_pos_gnd = y_pos

    
    
    pub.publish(message)


def apriltagProcessing():
    rospy.init_node('apriltag_data_processing', anonymous=True)

    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback0)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    apriltagProcessing()