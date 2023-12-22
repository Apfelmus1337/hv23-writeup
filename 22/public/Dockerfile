FROM ubuntu:22.04

RUN apt-get update -y && apt-get install -y socat

RUN useradd -d /home/santa/ -m -p santa -s /bin/bash santa
RUN echo "santa:santa" | chpasswd

WORKDIR /home/santa
COPY ./pwn .
COPY ./secret.txt .

USER santa

CMD socat TCP-LISTEN:1337,fork,reuseaddr EXEC:'./pwn',raw,pty,echo=0,stderr