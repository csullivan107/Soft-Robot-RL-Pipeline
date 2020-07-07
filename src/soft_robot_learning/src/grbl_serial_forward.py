#!/usr/bin/env python
import rospy,serial,time, sys
from std_msgs.msg import String


print(sys.version)

grblArduino = serial.Serial('/dev/ttyACM1', 115200, timeout=.1, exclusive=0)

print("serial information: ")
print("\t" + grblArduino.name)

#call back is called anytime the subscriber gets data from the topic
def callback(data):
    #str2send = String()
    str2send = "M8" + '\n' + data.data + '\n' + "M9" + '\n'
    rospy.loginfo(rospy.get_caller_id() + "I heard '%s' and am sending '%s'", data.data, str2send)
    
    grblArduino.write(str2send)
    
def grbl_forward():

    
    rospy.init_node('grbl_forward', anonymous=True)

    rospy.Subscriber("grbl_commands", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    grbl_forward()
