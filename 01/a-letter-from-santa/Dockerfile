FROM alpine:latest
RUN apk update
RUN apk add python3 py-pip
RUN pip --no-cache-dir install flask==3.0.0
COPY app.py /app/
COPY templates /app/templates
ENTRYPOINT ["python", "/app/app.py"]
