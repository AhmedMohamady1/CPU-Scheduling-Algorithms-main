from process import Process

class Algorithms:
    def __init__(self):
        pass
    
    def fcfs(processes):
        # Sort processes based on arrival time to ensure FCFS order
        processes.sort(key=lambda x: x.arrival_time)
        current_time = 0

        for process in processes:
            # If the CPU is idle, move the current time to the process's arrival time
            if current_time < process.arrival_time:
                current_time = process.arrival_time

            # Record the start and end times for the process
            start_time = current_time
            end_time = current_time + process.burst_time

            # Update the process's run intervals
            process.runs.append((start_time, end_time))
            current_time = end_time  # Advance the current time to the process's end time

            # Calculate performance metrics
            process.response_time = start_time - process.arrival_time  # Time from arrival to the start of execution
            process.turnaround_time = end_time - process.arrival_time  # Total time from arrival to completion
            process.waiting_time = process.turnaround_time - process.burst_time  # Time spent waiting in the ready queue

        # Return the list of processes with updated metrics
        return processes

    def sjf_preemptive(process_list: list):
        # Gantt_Chart list
        gantt_chart = []
        
        # dictionary holds the start and end time for each process execution
        time_intervals = {}    

        # define a list containing a completed processes
        completed_process = []

        # define a dictionary containing burst times of the processes to save them
        initial_burst_times = {}
        for p in process_list:
            initial_burst_times[p.p_id] = p.burst_time
        
        # initial time (first arrival time)
        t = sorted(process_list, key=lambda process: process.arrival_time)[0].arrival_time

        while len(process_list) != 0:
            # available processes in a specified time
            available = []

            for p in process_list:
                if p.arrival_time <= t:
                    available.append(p)

            t += 1

            if len(available) != 0:
                # sort the available processes by the burst_time
                available.sort(key=lambda process: process.burst_time)
                process = available[0]
                gantt_chart.append(process.p_id)
                process_list.remove(process)
                
                # updating the burst time of the process
                process.burst_time -= 1

                if process.burst_time == 0:
                    process.burst_time = initial_burst_times[process.p_id]
                    
                    # Completion Time
                    CT = t

                    # Turnaround Time
                    process.turnaround_time = CT - process.arrival_time

                    # Waiting Time
                    process.waiting_time = process.turnaround_time - process.burst_time

                    completed_process.append(process)

                else:
                    process_list.append(process)


        # the first arrival time
        first_arrival_time = sorted(completed_process, key=lambda process: process.arrival_time)[0].arrival_time
        
        # define boundaries for time intervals when a process was executed 
        min_time_boundary = first_arrival_time
        max_time_boundary = min_time_boundary + 1

        for i in range(len(gantt_chart)):
            if (i == len(gantt_chart) - 1) or (gantt_chart[i] != gantt_chart[i+1]): 
                if gantt_chart[i] not in time_intervals:
                    time_intervals[gantt_chart[i]] = []
                
                time_intervals[gantt_chart[i]].append([min_time_boundary, max_time_boundary])
                min_time_boundary = max_time_boundary

            max_time_boundary += 1 
        
        for p in completed_process:
            # assign the list of time intervals to runs list for each process 
            p.runs = time_intervals[p.p_id]

            # Response time
            p.response_time = p.runs[0][0] - p.arrival_time

        return completed_process
    
    def sjf_nonpreemptive(problem: list):
        current=0
        result=[]
        while problem:
            available=[]
            for i in problem:
                if i[2] <=current:
                    available.append(i)
            if available:
                sj=available[0]
                for i in available:
                    if i[1] < sj[1]:
                        sj=i
                problem.remove(sj)
                pName, burst_time, arrival_time = sj
                
                start_time = max(current, arrival_time)
                complete_time = start_time + burst_time
                turnaround_time = complete_time - arrival_time
                waiting_time = turnaround_time - burst_time
                response_time = start_time - arrival_time

                current = complete_time
                
                result.append([
                    pName, burst_time, arrival_time, 
                    start_time, complete_time, 
                    turnaround_time, waiting_time, 
                    response_time
                ])
            else:
                current_time += 1
        return result
    
    def round_robin(processes_ls:list[Process], qt:int):
        it = 0
        ls = []
        for i in processes_ls:
            i.sb = i.burst_time

        while (len(processes_ls) != 0):
            p = processes_ls.pop(0)
            if (p.burst_time > qt):
                p.burst_time -= qt
                it += qt
                p.runs.append([it-qt, it])
                processes_ls.append(p)
            else:
                it += p.burst_time
                p.runs.append([it-p.burst_time, it])
                p.burst_time = p.sb
                ct = p.runs[-1][1]
                st = p.runs[0][0]
                p.turnaround_time = ct - p.arrival_time
                p.waiting_time = p.turnaround_time - p.burst_time
                p.response_time = st - p.arrival_time
                ls.append(p)
        return ls

    def sort_runtimes(processes: list):
        runtimes=[]
        for process in processes:
            for run in process.runs:
                runtimes.append([process.p_id,run])      
        sorted_data = sorted(runtimes, key=lambda x: x[1][0])
        return sorted_data
    
    def calculate_averages(processes: list):
        n = len(processes)
        total_turnaround_time = sum(p.turnaround_time for p in processes)
        total_waiting_time = sum(p.waiting_time for p in processes)
        total_response_time = sum(p.response_time for p in processes)

        return {
            "average_turnaround_time": total_turnaround_time / n,
            "average_waiting_time": total_waiting_time / n,
            "average_response_time": total_response_time / n
        }