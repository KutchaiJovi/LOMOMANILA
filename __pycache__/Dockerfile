FROM python:3.6.8
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install python-mysqldb -y
RUN pip install -r requirements.txt
CMD ["python", "app.py"]