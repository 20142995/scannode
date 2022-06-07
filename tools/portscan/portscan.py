#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from celery import Celery
import masscan
import nmap

app = Celery(
    'portscan', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)

@app.task
def run(ips):
    result = []
    try:
        mas = masscan.PortScanner()
        mas.scan(ips.replace(',', ' '), ports='1-65535',
                 arguments='--rate 2000')
        for host in mas.all_hosts:
            for protocol in ["tcp", "udp"]:
                _port = list(map(str, mas[host].get(protocol, {}).keys()))
                if len(_port) == 0 or len(_port) > 300:
                    continue
                else:
                    try:
                        nm = nmap.PortScanner()
                        nm.scan(hosts=host, ports=",".join(
                            _port), arguments='-sV -Pn -n' if protocol == "tcp" else '-sU -sV -Pn -n')
                    except:
                        continue
                    for _host in nm.all_hosts():
                        for protocol in nm[_host].all_protocols():
                            for port in nm[_host][protocol].keys():
                                info = {}
                                info['ip_port'] = '{}:{}'.format(_host, port)
                                info['protocol'] = protocol
                                info['service'] = nm[_host][protocol][port].get(
                                    "name", "")
                                info['product'] = nm[_host][protocol][port].get(
                                    "product", "")
                                info['vsersion'] = nm[_host][protocol][port].get(
                                    "version", "")
                                result.append(info)
    except:
        pass

    return {'tool': 'portscan', 'result': result}


if __name__ == '__main__':
    print(run('8.8.8.8'))
