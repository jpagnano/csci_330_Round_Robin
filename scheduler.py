#! /usr/bin/env python
'''
Adam Saland
CSCI 330
Command line interface for cpu scheduling simulations
'''
import sys
from optparse import OptionParser
import random

parser = OptionParser()
parser.add_option("-s", "--seed", default=0, help="random", action="store", type="int", dest="seed")
parser.add_option("-p", "--procs", default=3, help="number of processes to generate", action="store", type="int", dest="procs")
parser.add_option("-l", "--plist", default="", help="input a comma-separated list of processes", action="store", type="string", dest="plist")
parser.add_option("-m", "--maxlen", default=10, help="max process time", action="store", type="int", dest="maxlen")
parser.add_option("-a", "--algorithm", default="RR", help="Choose Algorithm from: SJF, FIFO, RR", action="store", type="string", dest="algorithm")
parser.add_option("-q", "--quantum", default=1, help="Round Robin time quantum", action="store", type="int", dest="quantum")
parser.add_option("-c", "--compute", default=False, help="compute", action="store_true", dest="solve")

(options, args) = parser.parse_args()

random.seed(options.seed)

#show options chosen
print('ARG algorithm', options.algorithm)
if options.plist == '':
    print('ARG procs', options.procs)
    print('ARG maxlen', options.maxlen)
    print('ARG seed', options.seed)
else:
    print('ARG plist', options.plist)

print('')

import operator

#initialize proccess list variable
proclist = []

#load processes
if options.plist == '':
    for pid in range(0,options.procs):
        proc_runtime = int(options.maxlen * random.random()) + 1
        proclist.append([pid, proc_runtime])
        print('pid: {}, burst_time: {}'.format(pid, proc_runtime))

else:
    pid = 0
    for proc_runtime in options.plist.split(','):
        proclist.append([pid, float(proc_runtime)])
        pid += 1
    for proc in proclist:
        print('pid : {}, burst_time: {}'.format(proc[0], proc[1]))

print('\n')

#Solve by algorithm chosen
if options.solve == True:
    #Shortest Job first
    if options.algorithm == 'SJF':
        proclist = sorted(proclist, key=operator.itemgetter(1))
        options.algorithm = 'FIFO'

    #First in First Out
    if options.algorithm == 'FIFO':
        curr_time = 0
        print('Execution trace:')
        for proc in proclist:
            print('[ time: {} ] run proccess {} for {} secs, burst_completion: {}'.format(curr_time, proc[0], proc[1], curr_time + proc[1]))
            curr_time += proc[1]
        #Print Simulation Statistics
        print('\nSimulation Statistics:')
        curr_time     = 0.0
        count = 0
        turnaround_time_sum = 0.0
        wait_time_sum       = 0.0
        response_time_sum   = 0.0
        for tmp in proclist:
            pid  = tmp[0]
            proc_runtime = tmp[1]
            response_time   = curr_time
            turnaround_time = curr_time + proc_runtime
            wait_time       = curr_time
            print('pid: {} | resonse: {} | turnaround: {} | wait: {}'.format(pid, response_time, turnaround_time, wait_time))
            response_time_sum   += response_time
            turnaround_time_sum += turnaround_time
            wait_time_sum       += wait_time
            curr_time += proc_runtime
            count = count + 1
        print('Average: resonse: {} | turnaround: {} | wait: {}'.format(response_time_sum/count, turnaround_time_sum/count, wait_time_sum/count))

############# Round Robin ###############
    if options.algorithm == 'RR':
        #Trace iterations
        print('Execution trace:')
        turnaround_time = {}
        response_time = {}
        lastran_time = {}
        wait_time = {}
        quantum  = float(options.quantum)
        proccount = len(proclist)
        for i in range(0,proccount):
            lastran_time[i] = 0.0
            wait_time[i] = 0.0
            turnaround_time[i] = 0.0
            response_time[i] = -1

        runlist = []
        for e in proclist:
            runlist.append(e)

        curr_time  = 0.0
        #Iterate through process list subtracting the time quantum until the list is empty
        while proccount > 0:
            print('%d procs remaining' % proccount)
            proc = runlist.pop(0)
            pid  = proc[0]
            proc_runtime = float(proc[1])
            if response_time[pid] == -1:
                response_time[pid] = curr_time
            curr_wait = curr_time - lastran_time[pid]
            wait_time[pid] += curr_wait
            if proc_runtime > quantum:
                proc_runtime -= quantum
                burst_run_time = quantum
                print('[ time {} ] burst_run_time pid: {} | burst: {} secs'.format(curr_time, pid, burst_run_time))
                runlist.append([pid, proc_runtime])
            else:
                burst_run_time = proc_runtime;
                print('[ time {} ] burst_run_time pid: {} | burst: {} secs | burst_completion: {}'.format(curr_time, pid, burst_run_time, curr_time + burst_run_time))
                turnaround_time[pid] = curr_time + burst_run_time
                proccount -= 1
            curr_time += burst_run_time
            lastran_time[pid] = curr_time
        ##### Print Round Robin Simulation Statistics #####
        print('\nSimulation Statistics:')
        turnaround_time_sum = 0.0
        wait_time_sum       = 0.0
        response_time_sum   = 0.0
        for i in range(0,len(proclist)):
            turnaround_time_sum += turnaround_time[i]
            response_time_sum += response_time[i]
            wait_time_sum += wait_time[i]
            print('pid: {} | resonse: {} | turnaround: {} | wait: {}'.format(i, response_time[i], turnaround_time[i], wait_time[i]))
        count = len(proclist)
        print('Average: response: {}, turnaround: {},  wait: {}\n'.format(response_time_sum/count, turnaround_time_sum/count, wait_time_sum/count))
        #print('\nAverage -- Response: %3.2f  Turnaround %3.2f  Wait %3.2f\n' % (response_time_sum/count, turnaround_time_sum/count, wait_time_sum/count))

    if options.algorithm != 'FIFO' and options.algorithm != 'SJF' and options.algorithm != 'RR':
        print('Error: Policy', options.algorithm, 'is not available.')
        sys.exit(0)
else:
    print('Give it a shot and try to compute it by hand, if you cant figure it out, or want to see the use the -c flag to run computations')
