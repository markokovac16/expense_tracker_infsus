FROM python:3.9-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python", "app.py"]