#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from celery import Celery
import dns.resolver

app = Celery(
    'domaininfo', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)

def get_ip(domain, log_flag = True):
    domain = domain.strip()
    ips = []
    try:
        answers = dns.resolver.resolve(domain, 'A')
        for rdata in answers:
            ips.append(rdata.address)
    except dns.resolver.NXDOMAIN as e:
        if log_flag:
            print("{} {}".format(domain, e))

    except Exception as e:
        if log_flag:
            print("{} {}".format(domain, e))
    return ips

def get_cname(domain, log_flag = True):
    cnames = []
    try:
        answers = dns.resolver.resolve(domain, 'CNAME')
        for rdata in answers:
            cnames.append(str(rdata.target).strip(".").lower())
    except dns.resolver.NoAnswer as e:
        if log_flag:
            print(e)
    except Exception as e:
        if log_flag:
            print("{} {}".format(domain, e))
    return cnames

@app.task
def run(domains):
    result = []
    for domain in domains.split(','):
        ips = get_ip(domain)
        if not ips:
            ips = []
        cnames = get_cname(domain, False)
        info = {
            "domain": domain,
            "type": "A",
            "record": ips,
            "ips": ips
        }
        if cnames:
            info["type"] = 'CNAME'
            info["record"] = cnames
        result.append(info)
    return {'tool': 'domaininfo', 'result': result}


if __name__ == '__main__':
    print(run('www.baidu.com'))
