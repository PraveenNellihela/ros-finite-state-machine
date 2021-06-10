#!/usr/bin/env python3

import rospy
from ros_training_2.srv import (TriggerTransition, TriggerTransitionResponse)
from transitions import Machine


class StateMachine(object):
    def __init__(self):
        self.states = ['00', '11', '22', '33']
        self.transitions = [
            {'trigger': '0', 'source': '00', 'dest': '00'},
            {'trigger': '0', 'source': '11', 'dest': '00'},
            {'trigger': '0', 'source': '22', 'dest': '00'},
            {'trigger': '0', 'source': '33', 'dest': '00'},
            {'trigger': '1', 'source': '00', 'dest': '11'},
            {'trigger': '2', 'source': '11', 'dest': '22'},
            {'trigger': '3', 'source': '22', 'dest': '33'},
        ]
        self.machine = Machine(model=self, states=self.states,
                               transitions=self.transitions, initial='00')

    def fsm_handler(self, req):

        rospy.loginfo('trying to change state with trigger {}'.format(req.transition))
        try:
            self.trigger(str(req.transition))
            print('bot is now in state: ', self.state)
        except:
            print('cannot move to that state')
            success = False
            state = self.state
        else:
            success = True
            state = self.state

        response = success, int(state)
        return response

def main():
    rospy.init_node('fsm_server')
    fsm = StateMachine()
    while True:
        t = input('enter state ')

        s = rospy.Service('fsm_handler', TriggerTransition, fsm.fsm_handler)
        fsm_call = rospy.ServiceProxy('fsm_handler', TriggerTransition)
        fsm_call((int(t)))
        s.shutdown()
       # s.spin()

if __name__ == '__main__':
    main()
