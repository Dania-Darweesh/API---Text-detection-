FROM tiangolo/uvicorn-gunicorn-fastapi:python3.6

COPY requirements.txt /
RUN python -m pip install -r /requirements.txt

RUN apt-get update ##[edited]
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y

COPY ./app /app

