#!usr/bin/env python3
import rospy
from ros_training_2.msg import State
from ros_training_2.srv import TriggerTransition, TriggerTransitionResponse, TriggerTransitionRequest
from transitions import Machine

f = rospy.get_param('frequency')


class FSM(object):
    def __init__(self):
        self.pub = rospy.Publisher("~state", State, queue_size=10)
        self.serv = rospy.Service("~trigger", TriggerTransition, self.service_callback)
        self.timer = rospy.Timer(rospy.Duration(f), self.my_callback)
        self.state = State.START

        self.states = [str(State.START), str(State.ATLOC1), str(State.ATLOC2),
                       str(State.GRASPED_OBJ), str(State.PLACED_OBJ)]
        self.transitions = [
            {'trigger': str(TriggerTransitionRequest.RESET), 'source': str(State.ATLOC1), 'dest': str(State.START)},
            {'trigger': str(TriggerTransitionRequest.RESET), 'source': str(State.ATLOC2), 'dest': str(State.START)},
            {'trigger': str(TriggerTransitionRequest.RESET), 'source': str(State.GRASPED_OBJ), 'dest': str(State.START)},
            {'trigger': str(TriggerTransitionRequest.RESET), 'source': str(State.PLACED_OBJ), 'dest': str(State.START)},
            {'trigger': str(TriggerTransitionRequest.MOVE_1), 'source': str(State.START), 'dest': str(State.ATLOC1)},
            {'trigger': str(TriggerTransitionRequest.MOVE_1), 'source': str(State.PLACED_OBJ), 'dest': str(State.ATLOC1)},
            {'trigger': str(TriggerTransitionRequest.MOVE_2), 'source': str(State.ATLOC1), 'dest': str(State.ATLOC2)},
            {'trigger': str(TriggerTransitionRequest.GRASP), 'source': str(State.ATLOC2), 'dest': str(State.GRASPED_OBJ)},
            {'trigger': str(TriggerTransitionRequest.PLACE), 'source': str(State.GRASPED_OBJ), 'dest': str(State.PLACED_OBJ)},
        ]
        self.machine = Machine(model=self, states=self.states,
                               transitions=self.transitions, initial=str(State.START))
        rospy.spin()

    def service_callback(self, req):
        rospy.loginfo('trigger service: trying to change state with trigger {}'.format(req.transition))
        response = TriggerTransitionResponse()
        try:
            self.trigger(str(req.transition))
        except:
            response.success = False
            response.state.state = int(self.state)
        else:
            response.success = True
            response.state.state = int(self.state)
        return response
        rospy.spin()

    def my_callback(self, event):
        self.pub.publish(int(self.state))
        rospy.loginfo('current state ' + str(self.state) + ', current time ' + str(event.current_real))


if __name__ == "__main__":
    rospy.init_node("fsm")
    my_fsm = FSM()
