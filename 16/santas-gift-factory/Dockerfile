FROM ubuntu:23.04

RUN apt update && apt -y upgrade
RUN apt install -y socat

COPY . .

RUN chmod +x vuln
RUN chmod +x magic.sh

ENTRYPOINT socat TCP-LISTEN:1337,reuseaddr,fork EXEC:'./vuln',raw
