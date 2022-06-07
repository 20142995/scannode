#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import socket
from celery import Celery

FILEPATH = os.path.dirname(os.path.abspath(__file__))

app = Celery(
    'rad', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)

def check(ip_port):
    ip,port = ip_port.split(':')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(ip),int(port)))
        sock.close()
    except:
        return False
    else:
        return True

@app.task
def run(url,xray=False):
    result = []
    out_file_name = os.path.join(FILEPATH, '{}.json'.format(time.time()))
    radcmd = [os.path.join(FILEPATH,'rad_linux_amd64'), "-t", url,"--json-output",out_file_name]
    if xray and check("127.0.0.1:7777"):
        radcmd += ["--http-proxy", "127.0.0.1:7777"]
    os.system(' '.join(radcmd))
    if os.path.exists(out_file_name):
        for line in open(out_file_name,'r',encoding='utf8').readlines():
            try:
                rj = json.loads(line.strip().rstrip(','))
                result.append({'url':rj['URL'],'method':rj['Method'],'header':rj['Header'],'b64_body':rj.get('b64_body','')})
            except Exception as e:
                pass
        try:
            os.remove(out_file_name)
        except Exception as e:
            pass
    return {'tool': 'rad', 'result': result}

if __name__ == '__main__':
    print(run('http://127.0.0.1:60082/'))
