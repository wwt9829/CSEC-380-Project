FROM python:latest

COPY /flask/requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir video
COPY /flask .

CMD python chaimtube.py