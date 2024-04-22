FROM python:3.11-slim

WORKDIR /app

RUN apt-get update 

RUN apt-get install -y git

RUN apt-get install -y gcc

RUN apt-get install -y default-libmysqlclient-dev

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["flask", "db", "init"]
CMD ["flask", "db", "migrate"]
CMD ["flask", "db", "upgrade"]

EXPOSE 2247

CMD ["python", "run.py"]
