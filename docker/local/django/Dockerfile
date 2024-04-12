FROM python:3.10

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt .

RUN addgroup --system django \
    && adduser --system --ingroup django django

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

COPY ./docker/local/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

EXPOSE 8000

EXPOSE 2181

EXPOSE 6380

USER django

ENTRYPOINT ["/entrypoint"]
