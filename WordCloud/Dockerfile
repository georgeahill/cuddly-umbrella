FROM python:3.8-slim-buster

EXPOSE 8000

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "--log-level=debug"]