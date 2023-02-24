FROM python:3.9-slim-buster

WORKDIR /app

RUN chmod 777 /app

COPY requirements.txt .

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get upgrade -y
RUN apt -qq update --fix-missing && \
    apt -qq install -y \
    mediainfo

COPY . .

CMD [ "python3", "bot.py" ]
