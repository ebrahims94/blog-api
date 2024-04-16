FROM python:3.10

RUN apt-get update \
    && apt-get install -y \
        libpq-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD ["bash", "/app/start.sh"]