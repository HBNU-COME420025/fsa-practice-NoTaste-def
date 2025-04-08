from pyevsim import BehaviorModelExecutor, SystemSimulator, Infinite
import datetime

class PEx(BehaviorModelExecutor):
    def __init__(self, instance_time, destruct_time, name, engine_name):
        BehaviorModelExecutor.__init__(self, instance_time, destruct_time, name, engine_name)
        self.init_state("q0")
        self.insert_state("q0", Infinite)
        self.insert_state("q1", Infinite)
        self.insert_state("invalid", Infinite)

        self.insert_input_port("event")
        
        self.alphanumeric = "abcdefghijklmnopqrstuvwxyz0123456789"
        self.alpha = "abcdefghijklmnopqrstuvwxyz"

    def ext_trans(self,port, msg):
        if port == "event":
            event = msg.retrieve()[0]
            print(event)
            if self._cur_state == "q0":
                if event in self.alpha:
                    print("ACCEPT")
                    self._cur_state = "q1"
                else:
                    print("NOT ACCEPT")
                    self._cur_state = "invalid"
            elif self._cur_state == "q1":
                if event in self.alphanumeric:
                    print("ACCEPT")
                    self._cur_state = "q1"
                else:
                    print("NOT ACCEPT")
                    self._cur_state = "invalid"
                

    def output(self):
        return None
        
    def int_trans(self):
        if self._cur_state == "q1":
            self._cur_state = "q1"
        elif self._cur_state == "q0":
            self._cur_state = "q0"
        else:
            self._cur_state = "invalid"


ss = SystemSimulator()

ss.register_engine("first", "REAL_TIME", 1)
ss.get_engine("first").insert_input_port("event")
gen = PEx(0, Infinite, "Gen", "first")
ss.get_engine("first").register_entity(gen)

ss.get_engine("first").coupling_relation(None, "event", gen, "event")

event_string = "qwer1234"
for alpha in event_string:
    ss.get_engine("first").insert_external_event("event", alpha)
    ss.get_engine("first").simulate(1)


