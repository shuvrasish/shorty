FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN addgroup --system shorty \
    && adduser --system --ingroup shorty shorty

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY ./zookeeper/setup.py /app

RUN chown shorty:shorty /app

USER shorty

CMD ["python","setup.py"]
