#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from celery import Celery

app = Celery(
    'jsfinder', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)


@app.task
def run(urls):
    result = []
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    in_file_name = os.path.join(FILEPATH, '{}.txt'.format(time.time()))
    with open(in_file_name, 'w', encoding='utf8') as f:
        for url in urls:
            url = url if '://' in url else 'http://'+url
            f.write('{}\n'.format(url))
    out_file_name = os.path.join(FILEPATH, '{}.txt'.format(time.time()))
    os.system("cd {} && python3 _JSFinder.py -f {} -ou {}".format(FILEPATH,
              in_file_name, out_file_name))
    if os.path.exists(out_file_name):
        with open(out_file_name, 'r') as f:
            for line in f.readlines():
                if line.strip():
                    info = {}
                    info['url_full'] = line.strip()
                    result.append(info)

    try:
        os.remove(in_file_name)
    except Exception as e:
        pass
    try:
        os.remove(out_file_name)
    except Exception as e:
        pass
    return {'tool': 'jsfinder', 'result': result}


if __name__ == '__main__':
    print(run(['https://www.baidu.com']))
