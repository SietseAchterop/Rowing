#!/usr/bin/env python

from trac_ik_python.trac_ik import IK

ik_solver = IK("skiff",  "dummy_link_1")

print(ik_solver.base_link)
print(ik_solver.tip_link)
print(ik_solver.link_names)
print(ik_solver.joint_names)

