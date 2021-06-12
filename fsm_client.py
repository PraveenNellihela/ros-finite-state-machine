#!/usr/bin/env python3

import rospy
from ros_training_2.srv import TriggerTransition

def fsm_client(transition):
    print('now in fsm_client')
    rospy.wait_for_service('~trigger')
    try:
        fsm_server = rospy.ServiceProxy('~trigger', TriggerTransition)
        response = fsm_server(transition)
        print('fsm_client response is :'.format(response))
        return response
    except rospy.ServiceException as e:
        print('Service call failed. %s', e)


if __name__ == '__main__':
    rospy.init_node('fsm_client')
    t = input('enter transition: ')
    print('now in state: %s' % fsm_client(int(t)))

