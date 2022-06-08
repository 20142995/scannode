#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import json
from celery import Celery


app = Celery('ehole', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER = 'json',CELERY_RESULT_SERIALIZER = 'json',CELERY_ACCEPT_CONTENT=['json'],CELERY_TIMEZONE = 'Asia/Shanghai',CELERY_ENABLE_UTC = False,)


@app.task
def run(urls):
    result = []
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    in_file_name = os.path.join(FILEPATH,'{}.txt'.format(time.time()))
    with open(in_file_name,'w',encoding='utf8') as f:
        for url in urls:
            url = url if '://' in url else 'http://'+url
            f.write('{}\n'.format(url))
    out_file_name = os.path.join(FILEPATH,'{}.json'.format(time.time()))
    os.system("cd {} && ./Ehole3.0-linux -l {} -json {}".format(FILEPATH, in_file_name,out_file_name))
    if os.path.exists(out_file_name):
         with open(out_file_name, 'r') as f:
            for line in f.readlines():
                try:
                    item = json.loads(line)
                    info = {}
                    info['url'] = item['url']
                    info['status_code'] = item['statuscode']
                    info['title'] = item['title']
                    info['content_length'] = item['length']
                    info['cms'] = item['cms']
                    info['raw_response'] = item['server']
                    result.append(info)
                except:
                    pass
    try:
        os.remove(in_file_name)
    except Exception as e:
        pass
    try:
        os.remove(out_file_name)
    except Exception as e:
        pass
    return {'tool':'ehole','result':result}

if __name__ == '__main__':
    print(run(['https://www.baidu.com']))
