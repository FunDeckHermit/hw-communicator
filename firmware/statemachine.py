from machine import Timer
import time

class LinearStateMachine:
    def __init__(self, n_states):
        self.index = 0
        self.n_states = n_states
        self.lasttransition = time.ticks_ms()
    
    def __str__(self):
        timepassed = time.ticks_ms() - self.lasttransition
        return f'Current state: {self.index}'
    
    def next_state(self):
        self.index = (self.n_states + self.index + 1) % self.n_states
        self.lasttransition = time.ticks_ms()
    
    def prev_state(self):
        self.index = (self.n_states + self.index - 1) % self.n_states
        self.lasttransition = time.ticks_ms()   
    
    def reset(self):
        self.index = 0



class WaitTimeStateMachine(LinearStateMachine):
    def __init__(self, n_states):
        super().__init__(n_states)
        self.waittimes = [-1 for x in range(n_states)]
        self.autoadvances = [False for x in range(n_states)]
        self.oneshottimer = Timer()
        
    def setwaittime(self, state_index, waittime, auto = False):
        if state_index >= 0 and state_index < self.n_states:
            self.waittimes[state_index] = waittime
            self.autoadvances[state_index] = auto
            self.oneshottimer = Timer()
            
    def next_state(self):
        wt = self.waittimes[self.index]
        if wt is -1:
            self.conditional_advance(self)
            return
        self.oneshottimer.deinit()
        self.oneshottimer.init(mode=Timer.ONE_SHOT, period=wt, callback=self.advance)
     
    def advance(self, *_):
        super().next_state()
        self.check_auto_next()
        
    def check_auto_next(self):
        if self.autoadvances[self.index]:
            self.next_state()
            


class CallbackWaitingStateMachine(WaitTimeStateMachine):
    def __init__(self, n_states):
        super().__init__(n_states)
        self.callbacks = [None for x in range(n_states)]   

    def setwaitcallback(self, state_index, waittime, callback, auto = False):
        super().setwaittime(state_index, waittime, auto)
        self.setcallback(state_index, callback)
 
    def setcallback(self, state_index, callback):
        if state_index >= 0 and state_index < self.n_states:
            self.callbacks[state_index] = callback                    
        
    def next_state(self):
        super().next_state()
    
    def advance(self, *_):
        if self.callbacks[self.index] and self.callbacks[self.index]() == False:
            """Callback set but unsuccesfull"""
            return        
        super().advance()
        
        
