FROM python:3.6

ENV KERAS_BACKEND tensorflow

WORKDIR /workdir

ADD . .
RUN pip3 install -r requirements.txt
RUN python3 downloader.py

CMD ["python", "run.py"]
