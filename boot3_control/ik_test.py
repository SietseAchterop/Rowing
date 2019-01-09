#!/usr/bin/env python

from trac_ik_python.trac_ik import IK

ik_solver = IK("skiff",               "dummy_link_1")

print (ik_solver.number_of_joints)


print(ik_solver.base_link)
print(ik_solver.tip_link)
print(ik_solver.joint_names)


ik_solver.link_names

seed_state = [0.0] * ik_solver.number_of_joints

#print(ik_solver.get_ik(seed_state, -3.591, 0.191, 0.545,     0.345 ,0.935 ,0.068 ,0.037,       0.01, 0.01, 0.01,        0.1, 0.1, 0.1))
print(ik_solver.get_ik(seed_state, -3.361, 0.179, 0.553,     0.300 ,0.953 ,0.033 ,0.011,       0.1, 0.1, 0.1,        0.02, 0.02, 0.02))

