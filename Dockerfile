FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD python cities_API//manage.py migrate

CMD python cities_API//manage.py runserver 0.0.0.0:8000