FROM docker.io/library/ubuntu:23.04

RUN apt update && apt -y upgrade
RUN apt install -y socat

COPY . .

RUN chmod +x vuln

ENTRYPOINT ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:\"./vuln\""]
