FROM python:3.10

RUN mkdir /bot_app
WORKDIR /bot_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh

RUN alembic upgrade head

CMD gunicorn -w 1 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000 
