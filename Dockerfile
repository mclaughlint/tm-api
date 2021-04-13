FROM python:3.9.2-slim-buster
WORKDIR /app
RUN apt-get update
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
EXPOSE 5000
COPY . /app/

CMD ["python3", "api/run.py"]

