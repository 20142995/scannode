FROM ubuntu:18.04

ENV LANG C.UTF-8

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean && apt-get update 
RUN apt-get install -y python3 python3-pip nmap masscan language-pack-zh-hans fontconfig git wget 
RUN cd /tmp && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb

WORKDIR /app

ADD ./ /app
RUN pip3 install --upgrade pip -i  https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip3 install scikit-build -i  https://pypi.tuna.tsinghua.edu.cn/simple \
  && pip3 install cmake -i  https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r requirements.txt  -i  https://pypi.tuna.tsinghua.edu.cn/simple 

RUN cp tools/xray/ca.crt  /usr/local/share/ca-certificates/xray.crt && update-ca-certificates
# ADD docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
