#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
from celery import Celery


app = Celery(
    'ksubdomain', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)


@app.task
def run(domain):
    result = []
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    out_file_name = os.path.join(
        FILEPATH, 'tool', '{}.txt'.format(time.time()))
    exe = os.path.join(FILEPATH, 'tool', 'ksubdomain')
    os.system("{} -d {} -skip-wild -silent -o {}".format(exe, domain, out_file_name))
    if os.path.exists(out_file_name):
        with open(out_file_name, 'r') as f:
            for line in f.readlines():
                result.append({'domain':line.strip()})
    try:
        os.remove(out_file_name)
    except Exception as e:
        pass
    return {'tool': 'ksubdomain', 'result': result}


if __name__ == '__main__':
    print(run('baidu.com'))
