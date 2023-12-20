FROM alpine:latest
RUN apk update
RUN apk add python3 py3-flask
COPY app.py flag.txt /app/
COPY form_template.html index.html /app/templates/
ENTRYPOINT ["python", "/app/app.py"]