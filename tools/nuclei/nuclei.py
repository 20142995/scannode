#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import json
from celery import Celery

app = Celery('nuclei', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)

@app.task
def run(url):
    result = []
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    out_file_name = os.path.join(FILEPATH,'tool','{}.json'.format(time.time()))
    exe = os.path.join(FILEPATH,'tool', 'nuclei')
    os.system("{} -silent -json -u {} -o {}".format(exe, url,out_file_name))
    if os.path.exists(out_file_name):
         with open(out_file_name, 'r') as f:
            for line in f.readlines():
                item = json.loads(line)
                info = {}
                info['vuln_addr'] = item['host']
                info['vuln_name'] = item['info']['name']
                info['vuln_level'] = item['info']['severity']
                info['vuln_payload'] = item['matched-at']
                info['vuln_raw_response'] = line
                result.append(info)
    try:
        os.remove(out_file_name)
    except Exception as e:
        pass
    return {'tool': 'nuclei', 'result': result}


if __name__ == '__main__':
    print(run('https://www.baidu.com'))
