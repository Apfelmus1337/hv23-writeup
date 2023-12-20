FROM alpine:latest

RUN apk update
RUN apk add socat python3 py3-pycryptodome curl

WORKDIR /app
COPY firmware.zip chall.py flag .

ENTRYPOINT socat tcp-l:1337,reuseaddr,fork EXEC:"python3 chall.py"
