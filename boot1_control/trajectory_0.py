#!/usr/bin/env python

"""  trajectory voor boot1 

1 deze versie:
     parameterisen van de haal:tempo, haal/recover verhouding
   hoe recht laten gaan?
     sleuf, sturen, prismatic joint dus
   hoe verlopen de krachten tijdens de haal? wrijvingsparameters?


2 volgende:
   meerdere topics lezen en data verwerken
   eerst in array zetten 

   verwijderen en opnieuw laden model (met andere parameters!)
     ook programmatisch

 """


import numpy as np
import rospy
import actionlib

from control_msgs.msg import FollowJointTrajectoryAction, FollowJointTrajectoryGoal
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from sensor_msgs.msg import JointState
from gazebo_msgs.msg import ModelStates

# globals
# All joints to control
arm_joints = ['starboard_rowlock',
              'port_rowlock',
              'starboard_oar',
              'port_oar',
              'starboard_blade',
              'port_blade' ]
tfstart = 0

# Connect to the trajectory action server
rospy.loginfo('Waiting for boot1 trajectory controller...')
arm_client = actionlib.SimpleActionClient('boot1/joint_trajectory_controller/follow_joint_trajectory', FollowJointTrajectoryAction)

def jscallback(data):
    dummy=data
    #print ('position', data.position)
    # data to nparray
    # stop collecting when done

def boatposcb(data):
    print ('position.x %3.2f' % data.pose[1].position.x)

# main function
def main():
    rospy.init_node('trajectory_0')

    # subscribe to ...
    rospy.Subscriber("/boot1/joint_states", JointState, jscallback)
    rospy.Subscriber("/gazebo/model_states", ModelStates, boatposcb)

    # Set to True to move back to the starting configurations
    reset  = rospy.get_param('~reset', False)
    repeat = rospy.get_param('~repeat', 3)

    # connect to server
    arm_client.wait_for_server()
    rospy.loginfo('...connected.')
        
    # Set initial goal configurations for the boat
    move_goals  = [[0.0, -0.0, -0.0, 0.0, 0.0, -0.0]]
    time_goals  = [ 1.0]

    # describe a stroke cycle
    # use parameters?
    cycle_goals = [[0.8, -0.8, -0.10, 0.10, 0.02, -0.01],
                   [0.8, -0.8, -0.25, 0.24 , 0.02, -0.01],
                   [-0.55, 0.55, -0.25, 0.24 , 0.02, -0.01],
                   [-0.55, 0.55, -0.10, 0.10 , 0.02, -0.01]]
    cycle_times = [ 0.2, 1.0, 0.2, 2.0 ]

    # calculate complete session:
    for i in range(repeat):
        print ('Pass %d' % i)
        for j in range(len(cycle_goals)):
            move_goals.append(cycle_goals[j])
            time_goals.append(cycle_times[j])

    do_move(move_goals, time_goals)
    # sleep until movement completely done to collect the data
    rospy.sleep(tfstart+3)
    print ('Done', tfstart+3)
    # stop collecting and process the data

def do_move(move_goals, time_goals):
    global tfstart
    print ('Do move')

    # Create a single-point arm trajectory with the arm_goal as the end-point
    arm_trajectory = JointTrajectory()
    arm_trajectory.joint_names = arm_joints

    tfstart = 0
    for j in range(len(move_goals)):
        arm_goal = move_goals[j]
        tfstart = tfstart+time_goals[j]
        print (' move_goals[%d] %s' % (tfstart, arm_goal))
        
        arm_trajectory.points.append(JointTrajectoryPoint())
        arm_trajectory.points[j].positions = arm_goal
        arm_trajectory.points[j].velocities = [0.0 for i in arm_joints]
        arm_trajectory.points[j].accelerations = [0.0 for i in arm_joints]
        arm_trajectory.points[j].time_from_start = rospy.Duration(tfstart)
    
    # Send the trajectory to the arm action server
    rospy.loginfo('Start moving the boat, will take %0.1f seconds.' % tfstart)
        
    # Create an empty trajectory goal
    arm_goal = FollowJointTrajectoryGoal()
        
    # Set the trajectory component to the goal trajectory created above
    arm_goal.trajectory = arm_trajectory
        
    # Specify zero tolerance for the execution time
    arm_goal.goal_time_tolerance = rospy.Duration(0.0)
    
    # Send the goal to the action server
    arm_client.send_goal(arm_goal)
    arm_client.wait_for_result()   # why does this return immediately?
    print('klaar')

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
    
