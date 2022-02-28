FROM python:3.9.1
ADD . /work
WORKDIR /work
RUN pip install -r requirements.txt
CMD python main.py