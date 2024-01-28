FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

COPY . /app

# TODO: add commands for migrating flask db

EXPOSE 2247

CMD ["python", "run.py"]
