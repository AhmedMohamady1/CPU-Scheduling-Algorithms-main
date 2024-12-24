from algorithms import Algorithms

class Process:
    def __init__(self,p_id,arrival_time,burst_time, priority=None):
        self.p_id=p_id
        self.arrival_time=arrival_time
        self.burst_time=burst_time
        self.priority=priority
        self.runs=[]
        self.response_time=None
        self.waiting_time=None
        self.turnaround_time=None
                    
    def __str__(self):
        return f'Process ID: {self.p_id}\nArrival Time: {self.arrival_time}\nBurst Time: {self.burst_time}\nPriority: {self.priority}\nRuns: {self.runs}\nResponse Time: {self.response_time}\nWaiting Time: {self.waiting_time}\nTurnaround Time: {self.turnaround_time}'
    
if __name__=='__main__':
    processes=[Process('p1',0,8),Process('p2',1,4)]
    algorithms=Algorithms()
