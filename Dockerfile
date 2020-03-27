FROM python:3.7
WORKDIR /src/
COPY ./dags .
COPY requirements.txt .
RUN pip install -r requirements.txt