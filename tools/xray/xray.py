#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import threading
from dingtalk import send_text
from flask import Flask, request


app = Flask(__name__)

class crack(threading.Thread):
    def __init__(self,curr_time):
        threading.Thread.__init__(self)
        self.curr_time = curr_time
    def run(self):
        time.sleep(5)
        os.system("date -s "+self.curr_time)

@app.route('/webhook', methods=['POST'])
def xray_webhook():
    try:
        data = request.json
        data_type = data['type']
        vuln = data["data"]
    except:
        return 'error'
    if data_type == "web_vuln":
        info = {'addr':vuln["detail"]["addr"], 'plugin':vuln["plugin"],'payload':vuln["detail"]["payload"]}
        print(info)
        try:
            if os.environ.get('DINGTALK_TOKEN',''):
                send_text(str(info),token=os.environ['DINGTALK_TOKEN'],secret=os.environ.get('DINGTALK_SECRET',''))
        except Exception as e:
            pass
    return 'ok'
    
def flask_main():
    app.run(host='127.0.0.1',port=5000)

def main():
    webhook = threading.Thread(target=flask_main)
    webhook.daemon = True
    webhook.start()
    FILEPATH = os.path.dirname(os.path.abspath(__file__))
    xraypath = os.path.join(FILEPATH,'xray_linux_amd64')
    xraycmd = [xraypath, "webscan", "--listen", "127.0.0.1:7777", "--html-output", time.strftime("%Y-%m-%d-%H-%M-%S")+'.html',"--webhook-output","http://127.0.0.1:5000/webhook"]
    curr_time=time.strftime('%Y-%m-%d', time.localtime(time.time()))
    os.system("date -s 2022-02-09")
    thread1 = crack(curr_time)
    thread1.start()
    os.system(" ".join(xraycmd))

if __name__ == '__main__':
    main()
