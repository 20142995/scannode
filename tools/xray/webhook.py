#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from dingtalk import send_text
from flask import Flask, request

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def xray_webhook():
    try:
        data = request.json
        data_type = data['type']
        vuln = data["data"]
    except:
        return 'error'
    if data_type == "web_vuln":
        info = {'addr': vuln["detail"]["addr"],
                'plugin': vuln["plugin"], 'payload': vuln["detail"]["payload"]}
        print(info)
        try:
            if os.environ.get('DINGTALK_TOKEN', ''):
                send_text(str(info), token=os.environ['DINGTALK_TOKEN'], secret=os.environ.get(
                    'DINGTALK_SECRET', ''))
        except Exception as e:
            pass
    return 'ok'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
