#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import psutil
import argparse
import sched
import sys
import ctypes
import threading
import os

parser = argparse.ArgumentParser(description='oracle服务器保活程序')

parser.add_argument('-c', '--occupancy', dest='occu_rate', help='cpu占用率')
parser.add_argument('-p', '--persistent', dest='pertime',   help='占用时长(秒)')
parser.add_argument('-i', '--interval', dest='interval', help='间隔调用(分)')
parser.add_argument('-m' '--memory', dest='mem', help='占用内存(MB)')
parser.add_argument('-n', '--netinterval', dest='netinterval', help='网络占用的时间间隔(分钟)')
args = parser.parse_args()

if args.pertime is not None:
    time_limit = float(args.pertime)
    if time_limit <= 0:
        time_limit = 60

sc = sched.scheduler(time.time, time.sleep)
netsc = sched.scheduler(time.time, time.sleep)

if args.netinterval is not None:
    netinterval = int(args.netinterval)
    if netinterval <= 1:
        netinterval = 30

if args.mem is not None:
    mem = int(args.mem)
    if mem <= 0 :
        mem = 100

if args.occu_rate is not None:
    occu_rate = int(args.occu_rate)
    if occu_rate <= 1:
        occu_rate = 20

if args.interval is not None:
    interval = int(args.interval)
    if interval <= 0 :
        interval = 3
    

def main():
    size = 1024*1024*mem
    buffer = ctypes.create_string_buffer(size)
    sc.enter(1, 1, wasteCup, ())
    netsc.enter(1, 1, netWaste, ())
    t1 = threading.Thread(target=netsc.run)
    t2 = threading.Thread(target=sc.run)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def netWaste():
    os.system('speedtest-cli --simple > /tmp/net_speed_waste')

    netsc.enter(netinterval*60, 1, netWaste, ())

def wasteCup():
    start_time = time.time()
    while True:
        while True:
            x = 1.0

            for i in range(1, 100000):
                x = x * i
            cpu_usage = psutil.cpu_percent()
            if cpu_usage < occu_rate:
                continue
            else:
                time.sleep(0.05)
                break

       # print('判断时间，开始时间' + str(start_time) + ',结束时间:' + str(time.time()) + ',持续时间:'+str(time_limit))
        if  float(time.time()) - float(start_time) > float(time_limit):
            #print('大于持续时间')
            break

    print('进入下一次等待')
    sc.enter(interval*60, 1, wasteCup, ())


if __name__ == '__main__':
    if len(sys.argv) <= 1:
      parser.print_help()
      exit()
    
    main()
