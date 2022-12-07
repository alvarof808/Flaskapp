FROM ubuntu:22.04

MAINTAINER alvaro.flores.h@ucb.edu.bo

RUN apt update
RUN apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install virtualenv

RUN apt install tesseract-ocr -y
RUN apt install libtesseract-dev -y
RUN pip install flask-sqlalchemy
RUN pip install Flask-Migrate
RUN pip install psycopg2-binary

WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5555

CMD [ "python3", "app.py" ]

