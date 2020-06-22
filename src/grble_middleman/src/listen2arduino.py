
import rospy,serial,time
from std_msgs.msg import String

grblArduino = serial.Serial('/dev/ttyACM0', 115200, timeout=.1)

#call back is called anytime the subscriber gets data from the topic
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    str2send = data.data
    grblArduino.write(str2send.encode())
    
def grbl_forward():

    
    rospy.init_node('grbl_forward', anonymous=True)

    rospy.Subscriber("grbl_msgs", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    grbl_forward()