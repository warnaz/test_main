FROM python:3.10

RUN mkdir /bot_app
WORKDIR /bot_app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x *.sh

# CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker starknet.main:app --bind 0.0.0.0:8000 
