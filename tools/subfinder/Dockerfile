FROM python:3.6

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN chmod +x docker-entrypoint.sh

CMD /app/docker-entrypoint.sh

