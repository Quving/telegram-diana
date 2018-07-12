FROM python:3.6

WORKDIR /workdir

ADD . .
RUN pip install -r requirements.txt
RUN python downloader.py

CMD ["python", "run.py"]
