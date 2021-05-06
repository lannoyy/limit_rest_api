FROM ubuntu:20.04

WORKDIR /app/server

COPY requirements.txt /app/server
RUN apt-get update && apt install python3-pip -y
RUN pip3 install --upgrade pip -r requirements.txt
COPY . /app/server

CMD ["ls"]
RUN chmod 755 start.sh
ENTRYPOINT ["sh", "./start.sh"]

EXPOSE 8080