FROM python:3.8

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_ENV="production"

ENTRYPOINT ["python", "./main.py"]
