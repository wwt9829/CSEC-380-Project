FROM python:3.6

WORKDIR /flask

COPY requirements.txt /flask
RUN pip install -r requirements.txt

COPY app.py /flask
COPY . /flask
CMD python app.py