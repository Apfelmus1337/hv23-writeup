FROM ubuntu:22.04

# install nc
RUN apt-get update && apt-get install -y netcat

WORKDIR /app
COPY . /app

ENTRYPOINT ["bash", "bask.sh"]
