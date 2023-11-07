FROM ubuntu:22.04

MAINTAINER alvaro.flores.h

RUN apt update
RUN apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN pip3 install virtualenv

RUN apt install tesseract-ocr -y
RUN apt-get install tesseract-ocr-spa -y
RUN apt install libtesseract-dev -y
#RUN apt install sox ffmpeg libcairo2 libcairo2-dev -y
#RUN apt-get install texlive-full -y
#RUN pip3 install manimlib
#RUN pip3 install manimce
#RUN pip install flask-sqlalchemy Flask-Migrate psycopg2-binary


WORKDIR /app

COPY . /app

RUN pip3 --no-cache-dir install -r requirements.txt

RUN apt install cups-pdf -y
RUN apt install libreoffice -y
EXPOSE 5555
#RUN python3 models.py
RUN [ "python3", "models.py" ]

#CMD [ "python3", "models.py" ]
CMD [ "python3", "app.py" ]

