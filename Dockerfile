FROM python:3.9.5-buster

RUN apt update -y && \
    apt install -y iputils-ping net-tools

WORKDIR /usr/home/lecuop

CMD ["bash"]
