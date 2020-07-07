#!/usr/bin/env python
import rospy,serial,time, sys
from std_msgs.msg import String


print(sys.version)



grblArduino = serial.Serial('/dev/ttyACM1', 115200, timeout=.1, exclusive=0)

print("serial information: ")
print("\t" + grblArduino.name)

def grbl_listener():

	pub = rospy.Publisher('grbl_feedback', String, queue_size=100)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(1) # 1hz
	grblMsg = ""
	
	while not rospy.is_shutdown():
		if grblArduino.inWaiting():
			
			# while (grblArduino.inWaiting() > 0):
			# 	grblMsg = ""
			# 	grblMsg += grblArduino.read()

			grblMsg = grblArduino.read(grblArduino.inWaiting())

			#print("incoming grbl message: %s", grblMsg)
		else:
			grblMsg = "nothing from grbl controller"
		
		rospy.loginfo(grblMsg)
		pub.publish(grblMsg)

		grblMsg = ""
		rate.sleep()


        

if __name__ == '__main__':
    grbl_listener()

