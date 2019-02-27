#!/usr/bin/env python

"""
get joint states using joint_states_publisher
get tf between 2 links
calc trac_ik
write new settings to param file


"""

from __future__ import print_function
import math
import os
import numpy as np
import rospy
import tf
from sensor_msgs.msg import JointState
from trac_ik_python.trac_ik import IK

# start program
rospy.init_node('calc_new_positions', anonymous=True)

# run joint states publisher to get names and current positions from topic joint_states
js = JointState()

cbcount = 0
def callbackjs(data):
    global cbcount, js
    if cbcount < 2:
        js = data
        #print(js)
    cbcount +=1

rospy.Subscriber("joint_states", JointState, callbackjs)

# wait until js is being filled
while cbcount < 2:
    pass
    
number_of_joints = len(js.name)

# goal
fromlink = "world"
tolink   = "Rdummy_link_1"
# for this link
tolink2   = "Rdummy_link_2"

# hoe er voor zorgen dat niet alle links gebruikt worden? een speciale boot.xacro/launch_file gebruiken?


# tf code
listener = tf.TransformListener()

rate = rospy.Rate(10.0)
while not rospy.is_shutdown():
    try:
        (trans,rot) = listener.lookupTransform(fromlink, tolink, rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        continue
    
    print(trans)
    print(rot)
    break
    

ik_solver = IK(fromlink, tolink2, epsilon=1e-07)
seed_state = [0.0] * ik_solver.number_of_joints

res = ik_solver.get_ik(seed_state,
                       trans[0], trans[1], trans[2],
                       rot[0], rot[1], rot[2], rot[3] )   # of inverse??


if res != None:
    # a result!
    print("Link names: ")
    print(ik_solver.link_names)
    print()
    print("Joint names: ")
    print(ik_solver.joint_names)
    print(res)

    print("En nu dit wegschrijven in param file")

else:
    print("No result from trac_ik.")

