#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import requests
from celery import Celery

requests.packages.urllib3.disable_warnings()


app = Celery(
    'githubrepos', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)


@app.task
def run(keyword):
    result = []
    headers = {"Authorization": "token {}".format(os.environ.get('GITHUB_TOKEN',''))}
    try:
        rj = requests.get("https://api.github.com/repos/{}".format(keyword), headers=headers, verify=False).json()
        result.append({'html_url':rj['html_url'],'description':rj['description'],'updated_at':time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(rj['updated_at'], "%Y-%m-%dT%H:%M:%SZ"))})
        time.sleep(2)
    except:
        pass
    return {'tool': 'githubrepos', 'result': result}


if __name__ == '__main__':
    print(run('EdgeSecurityTeam/EHole'))
