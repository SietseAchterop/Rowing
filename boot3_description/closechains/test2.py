#!/usr/bin/env python

from trac_ik_python.trac_ik import IK

ik_solver = IK("seat", "dummy_link_1")

print(ik_solver.base_link)
# 'torso_lift_link'

print(ik_solver.tip_link)
# 'r_wrist_roll_link'

print(ik_solver.joint_names)
# ('r_shoulder_pan_joint', 'r_shoulder_lift_joint', 'r_upper_arm_roll_joint', 'r_elbow_flex_joint', 'r_forearm_roll_joint', 'r_wrist_flex_joint', 'r_wrist_roll_joint')

print(ik_solver.link_names)
# ('r_shoulder_pan_link', 'r_shoulder_lift_link', 'r_upper_arm_roll_link', 'r_upper_arm_link', 'r_elbow_flex_link', 'r_forearm_roll_link', 'r_forearm_link', 'r_wrist_flex_link', 'r_wrist_roll_link')

