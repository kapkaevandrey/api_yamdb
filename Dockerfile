FROM python:3.9.7

RUN mkdir /code

COPY requirements.txt /code

RUN python -m pip install --upgrade pip

RUN pip3 install -r /code/requirements.txt

COPY . /code

WORKDIR /code/api_yamdb

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000

LABEL authors='Andrey Kapkaev, Moskalev Anton, Shaposhnikov Anton' version=1.0
