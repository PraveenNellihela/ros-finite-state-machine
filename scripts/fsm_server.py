#!usr/bin/env python3
import rospy
from ros_training_2.msg import State
from ros_training_2.srv import TriggerTransition, TriggerTransitionResponse
from transitions import Machine


class FSM(object):
    def __init__(self):
        self.pub = rospy.Publisher("~state", State, queue_size=10)
        self.serv = rospy.Service("~trigger", TriggerTransition, self.service_callback)
        self.timer = rospy.Timer(rospy.Duration(0.5), self.my_callback)  # TODO: make parameter
        self.state = State.START
        rospy.spin()

        self.states = ['0', '1', '2', '3', '4']
        self.transitions = [
            {'trigger': '0', 'source': '1', 'dest': '0'},
            {'trigger': '0', 'source': '1', 'dest': '0'},
            {'trigger': '0', 'source': '2', 'dest': '0'},
            {'trigger': '0', 'source': '3', 'dest': '0'},
            {'trigger': '1', 'source': '0', 'dest': '1'},
            {'trigger': '1', 'source': '4', 'dest': '1'},
            {'trigger': '2', 'source': '1', 'dest': '2'},
            {'trigger': '3', 'source': '2', 'dest': '3'},
            {'trigger': '4', 'source': '3', 'dest': '4'},
        ]
        # triggers: 0=reset, 1=move-1, 2=move-2, 3=grasp
        # states: 00 =start, 11 = at-loc-1, 22=at-loc-2, 33 = grasped-obj
        self.machine = Machine(model=self, states=self.states,
                               transitions=self.transitions, initial='0')

    def run(self):
        rospy.spin()

    def service_callback(self, req):
        # TODO: implement handling of request here; includes FSM logic
        print('now in service_callback')
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
        response = TriggerTransition()
        response.state = int(state)
        response.success = success
        print('response is :'.format(response))
        return response
        rospy.spin()

    def my_callback(self, event):
        # TODO: implement publishing of state here; should be really thin
        self.pub.publish(self.state)
        print('Timer called at ' + str(event.current_real))


if __name__ == "__main__":
    rospy.init_node("fsm")
    my_fsm = FSM()
    #my_fsm.run()
