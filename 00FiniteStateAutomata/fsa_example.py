from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime

class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("Wait")
        self.insert_state("Wait", Infinite)
        self.insert_state("Check", Infinite)

        self.insert_input_port("event")

    def ext_trans(self,port, msg):
        if port == "event":
            print(msg.retrieve()[0])
            #self._cur_state = "check"

    def output(self):
        return None
        
    def int_trans(self):
        if self._cur_state == "check":
            self._cur_state = "check"


ss = SystemSimulator()

ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("event")
gen = PEx(0, Infinite, "Gen", "first")
ss.get_engine("first").register_entity(gen)

ss.get_engine("first").coupling_relation(None, "event", gen, "event")

event_string = "abc"
for alpha in event_string:
    ss.get_engine("first").insert_external_event("event", alpha)
    ss.get_engine("first").simulate(1)


