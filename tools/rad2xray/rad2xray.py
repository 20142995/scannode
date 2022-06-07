#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from celery import Celery
import subprocess
import threading
import json

FILEPATH = os.path.dirname(os.path.abspath(__file__))
global xray_over,rad_over,xray_start
xray_over = False
rad_over = False
xray_start = False



app = Celery(
    'rad2xray', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)

def xray_main(out_file_name):
    global xray_over,rad_over,xray_start
    print('[+] start xray')
    xraypath = os.path.join(FILEPATH,'tool','xray_linux_amd64')
    xraycmd = [xraypath, "webscan", "--listen", "127.0.0.1:57777", "--json-output", out_file_name]
    xray = subprocess.Popen(xraycmd,stdout=subprocess.PIPE, stdin=subprocess.PIPE,shell=False)
    for i in iter(xray.stdout.readline,'b'):
        print(i)
        if b'starting mitm server at 127.0.0.1' in i:
            xray_start = True
        if b'All pending requests have been scanned' in i and rad_over:
            xray.kill()
            break
            
    xray_over = True
    print('[+] end xray')

@app.task
def run(url):
    global xray_over,rad_over
    result = []
    out_file_name = os.path.join(FILEPATH, '{}.json'.format(time.time()))
    xray = threading.Thread(target=xray_main,args=(out_file_name,))
    xray.daemon = True
    xray.start()
    while not xray_start:
        pass
    print('[+] xray running')
    radcmd = [os.path.join(FILEPATH,'tool','rad_linux_amd64'), "-t", url, "--http-proxy", "127.0.0.1:57777"]
    print('[+] start rad')
    rad = subprocess.run(radcmd)
    rad_over = True
    print('[+] end rad')
    while not xray_over:
        pass
    if os.path.exists(out_file_name):
        for line in open(out_file_name,'r',encoding='utf8').readlines():
            try:
                rj = json.loads(line.strip().rstrip(','))
                result.append({'vuln_addr':rj['detail']['addr'],'vuln_name':rj['plugin'],'vuln_payload':rj['detail']['payload']})
            except:
                pass
        try:
            os.remove(out_file_name)
        except Exception as e:
            pass
    return {'tool': 'rad2xray', 'result': result}

if __name__ == '__main__':
    print(run('http://127.0.0.1:60082/'))
