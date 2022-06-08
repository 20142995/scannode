#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import threading


class crack(threading.Thread):
    def __init__(self, curr_time):
        threading.Thread.__init__(self)
        self.curr_time = curr_time

    def run(self):
        time.sleep(5)
        os.system("date -s "+self.curr_time)


def main():
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    xraypath = os.path.join(FILEPATH, 'xray_linux_amd64')
    xraycmd = [xraypath, "webscan", "--listen", "127.0.0.1:7777", "--html-output",
               time.strftime("%Y-%m-%d-%H-%M-%S")+'.html', "--webhook-output", "http://127.0.0.1:5000/webhook"]
    curr_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    os.system("date -s 2022-02-09")
    thread1 = crack(curr_time)
    thread1.start()
    os.system(" ".join(xraycmd))


if __name__ == '__main__':
    main()
