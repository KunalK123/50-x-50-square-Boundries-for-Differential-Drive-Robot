#!/usr/bin/env python3
import rospy
from gazebo_msgs.srv import ApplyJointEffort
from gazebo_msgs.srv import GetJointProperties
from gazebo_msgs.srv import GetModelState, GetModelStateRequest
import os
import time as t

msg_topic = '/gazebo/apply_joint_effort'
joint_left = 'left_wheel_hinge'
joint_right = 'right_wheel_hinge'

msg_topic_feedback = 'gazebo/get_joint_properties'

pub_feedback = rospy.ServiceProxy(msg_topic_feedback, GetJointProperties)

rospy.init_node('dd_ctrl')
pub = rospy.ServiceProxy(msg_topic,ApplyJointEffort)

effort = 0.4
start_time = rospy.Time(0,0)

f = 0.25
T = 1/f
end_time = rospy.Time(T,0)
rate = rospy.Rate(f)

#my_service = rospy.Service('/service_example_topic', Trigger, trigger_response)

robot_proxy = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

#def getRobotLocation():
#    global robot_proxy
#    a = GetModelStateRequest(model_name = 'robot')
#    a.model_name = "robot"
#    s = robot_proxy(a)
#    print s
#    x = s.pose.position.x
#    y = s.pose.position.y

#    return(x,y)
    


#def dropBox(x,y):
#    b0 = "./drop_box.sh"
#    b1 = name + str(box_1)
#    box_i += 1
#    b2 = str(x) + ""
#    b3 = str(y) + ""
#    b4 = "&"
#    buff = b0 + b1 + b2 + b3
#    os.system(buff)


while True:
      x = 0
      i = 1
      effort = -effort
      pub(joint_left, effort, start_time, end_time)
      pub(joint_right, effort, start_time, end_time)
      val = pub_feedback(joint_left)
      val2 = pub_feedback(joint_right)
      print("Left Wheel:", val.rate)
      print("Right Wheel:", val2.rate)
      rate.sleep()
      global robot_proxy
      a = GetModelStateRequest(model_name = 'robot')
      a.model_name = "robot"
      s = robot_proxy(a)
      print s
      x = s.pose.position.x
      if x < -1:
        b0 = "./drop_box.sh"
        b1 = str(i) + ""
        i += 1
        #b2 = str(x) + ""
        #b3 = "&"
        buff = b0 + " " + b1
        os.system(buff)
      else:
          continue 

      
