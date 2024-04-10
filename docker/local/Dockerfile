FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

EXPOSE 6380

CMD ["python","manage.py","runserver", "0.0.0.0:8000"]
