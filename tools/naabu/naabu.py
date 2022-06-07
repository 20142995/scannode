#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
from celery import Celery
from xml.dom.minidom import parse


app = Celery(
    'naabu', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)

@app.task
def run(ip,wordlist = 'top100'):
    result = []
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    nmap_file = os.path.join(FILEPATH,'naabu_result_{}.xml'.format(time.time()))
    naabu_nmap_cmd = 'nmap --version-all -n -Pn -T4 -oX {}'.format(nmap_file)
    out_file_name = os.path.join(FILEPATH,'{}_{}.json'.format(ip, time.time()))

    portfile = 'portfile_top100.txt'
    if(wordlist == 'top100'):
        portfile = 'portfile_top100.txt'
    elif(wordlist == 'top1000'):
        portfile = 'portfile_top1000.txt'
    elif(wordlist == 'all'):
        portfile = 'portfile_all.txt'

    command = "cd {} && ./naabu -host {} -ports-file {} -json -o {} -nmap-cli {}".format(ip,portfile,out_file_name,naabu_nmap_cmd)
    os.system(command)
    if os.path.exists(out_file_name):
        with open(out_file_name,'r',encoding='utf8') as f:
            for line in f.readlines():
                dic = {}
                try:
                    dic["host"] = str(json.loads(line)['host'])
                except:
                    pass
                dic["ip"] = str(json.loads(line)['ip'])
                dic["port"] = json.loads(line)['port']
                dic["service"] = ""
                result.append(dic)
    if os.path.exists(nmap_file):
        try:
            tree = parse(nmap_file);
            root = tree.documentElement
            port_length = len(root.getElementsByTagName('ports')[0].childNodes)
            for i in range(0, port_length, 2):
                server = root.getElementsByTagName('ports')[0].childNodes[i].childNodes[1].getAttribute("name")
                port = int(root.getElementsByTagName('ports')[0].childNodes[i].getAttribute("portid"))
                # 加入字典中
                for res in result:
                    if (port == res['port']):
                        res["service"] = str(server)
        except:
            pass
    try:
        os.remove(nmap_file)
    except Exception as e:
        pass
    try:
        os.remove(out_file_name)
    except Exception as e:
        pass
    return {'tool': 'naabu', 'result': result}


if __name__ == '__main__':
    print(run('127.0.0.1'))
