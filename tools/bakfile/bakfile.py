#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
from celery import Celery
import requests
from binascii import b2a_hex
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()

app = Celery(
    'bakfile', broker=os.environ['BROKER'], backend=os.environ['BACKEND'], )
app.conf.update(CELERY_TASK_SERIALIZER='json', CELERY_RESULT_SERIALIZER='json', CELERY_ACCEPT_CONTENT=[
                'json'], CELERY_TIMEZONE='Asia/Shanghai', CELERY_ENABLE_UTC=False,)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36', 'Connection': 'close'}


def try_get_title(url):
    rar_byte = '526172'
    zip_byte = '504b03'
    gz_byte = '1f8b080000000000000b'
    mysqldump_byte = '2d2d204d7953514c'
    phpmyadmin_byte = '2d2d207068704d794164'
    navicat_byte = '2f2a0a204e6176696361'
    adminer_byte = '2d2d2041646d696e6572'
    other_byte = '2d2d202d2d2d2d2d2d2d'
    navicat_MDT_byte = '2f2a0a4e617669636174'
    tar_gz_byte = '1f8b0800'
    url_full, status_code, title, = url, 0, 0
    try:
        r = requests.get(url=url, headers=headers, timeout=10,
                         allow_redirects=False, stream=True, verify=False)
        content = b2a_hex(r.raw.read(10)).decode()
        status_code = r.status_code
        if r.status_code == 200:
            rarsize = int(r.headers.get('Content-Length'))
            if rarsize >= 1024000000:
                unit = int(rarsize) // 1024 // 1024 / 1000
                rarsize = str(unit) + 'G'
            elif rarsize >= 1024000:
                unit = int(rarsize) // 1024 // 1024
                rarsize = str(unit) + 'M'
            else:
                unit = int(rarsize) // 1024
                rarsize = str(unit) + 'K'
            if content.startswith(rar_byte) or content.startswith(zip_byte) or content.startswith(gz_byte) or content.startswith(
                mysqldump_byte) or content.startswith(
                phpmyadmin_byte) or content.startswith(navicat_byte) or content.startswith(adminer_byte) or content.startswith(
                    other_byte) or content.startswith(navicat_MDT_byte) or content.startswith(tar_gz_byte):
                title = rarsize
            else:
                pass
        else:
            pass
    except Exception as e:
        pass
    return url_full, status_code, title


@app.task
def run(url):
    result = []
    url = url if '://' in url else 'http://'+url
    url = url if not url.endswith('/') else url.rstrip('/')
    url_full, status_code, title = try_get_title(url)
    if status_code != 0:
        host = urlparse(url).netloc
        if ':' in host:
            host = host.split(':')[0]
        keywords = []
        if not host.replace('.', '').isnumeric():
            keywords.append(host)
            keywords += host.split('.')
        keywords += ['1', '2', 'bf', 'beifen', 'wwwroot', 'wwwroot.sql', 'bbs', 'bak',
                     'backup', 'www', 'web', 'root', 'index', 'bf', '2018', '2019', '2020', '2021', '2022']

        suffixFormat = ['.rar', '.zip', '.gz', '.sql.gz',
                        '.tar.gz', '.sql', '.tar.tgz', '.bak']
        urls = []
        for i in set(keywords):
            for j in suffixFormat:
                urls.append('{}/{}{}'.format(url, i, j))
        pool = ThreadPoolExecutor(max_workers=10)
        for url_full, status_code, title in pool.map(try_get_title, urls):
            if title:
                info = {}
                info['url_full'] = url_full
                info['status_code'] = status_code
                info['title'] = title
                result.append(info)
    return {'tool': 'bakfile', 'result': result}


if __name__ == '__main__':
    print(run('https://www.baidu.com'))
