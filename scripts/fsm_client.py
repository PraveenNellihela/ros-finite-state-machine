#!/usr/bin/env python3

import rospy
from ros_training_2.srv import TriggerTransition


def fsm_client(transition):
    rospy.wait_for_service('/fsm_server/trigger')
    try:
        fsm_server = rospy.ServiceProxy('/fsm_server/trigger', TriggerTransition)
        if fsm_server(transition).success:
            print('transition was successful')
        else:
            print('cannot transition to given state from current state')
        print('Current state is ', fsm_server(transition).state, '\n')
    except rospy.ServiceException as e:
        print('Service call failed. %s', e)


if __name__ == '__main__':
    rospy.init_node('fsm_client')
    while not rospy.is_shutdown():
        t = input('enter state to transition to: ')
        if t == 'exit':
            break
        else:
            fsm_client(int(t))


