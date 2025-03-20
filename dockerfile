FROM python:latest

WORKDIR /Server

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV SECRET_APP_KEY = "6EzsDR7mCPvnwLQDLMR2n7DrSvVkEHpN"

EXPOSE 5000

CMD ["python", "main.py"]

#CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:5000", "main:app", "--access-logfile", "-", "--error-logfile", "-"]