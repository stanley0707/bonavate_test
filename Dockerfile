FROM python:3.8

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
COPY . /code/

RUN python -m pip --no-cache-dir install --upgrade pip setuptools \
    && python -m pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py collectstatic --clear --no-input && \
    python manage.py migrate && \
    gunicorn bonavate_test.asgi:application -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
