"""
Learning how to use multiprocessing and psutil to analyze cpu and mem usage
"""
from datetime import datetime
from multiprocessing import Process
import psutil, random, time

def func1():
    # print('func1: starting')
    tab = []
    for i in range(1000000):
        tab.append(random.randint(1, 10000))
    tab.sort()
    # print('func1: finishing')
    return tab

def func2(pid):
    pr = psutil.Process(pid=pid)
    # print('func2: starting')
    print("type,time,cpupercent,cputime_user,cputime_system,rss,vms,pfaults,pageins,mempercent")
    while psutil.pid_exists(pid):
        print(f"1,{datetime.now()},{pr.cpu_percent()},{pr.cpu_times().user},{pr.cpu_times().system},{pr.memory_info().rss},{pr.memory_info().vms},{pr.memory_info().pfaults},{pr.memory_info().pageins},{pr.memory_percent()}")
        time.sleep(0.1)
    # print('func2: finishing')

if __name__ == '__main__':
    # P1 and P2 will have different pids
    p1 = Process(target=func1)
    p1.start()
    p2 = Process(target=func2, args=(p1.pid,))
    p2.start()

    p1.join()
    p2.join()