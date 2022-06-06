#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from celery import Celery
import requests

app = Celery(
    'area', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)


@app.task
def run(ips):
    result = []
    for ip in ips.split(','):
        area = requests.get(
            'https://whois.pconline.com.cn/ip.jsp?ip={}'.format(ip)).text.strip()
        result.append({'ip':ip,'area':area})
    return {'tool': 'area', 'result': result}


if __name__ == '__main__':
    print(run('8.8.8.8'))
