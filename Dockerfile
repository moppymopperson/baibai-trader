FROM python:alpine
ADD . /bitbaibai
WORKDIR /bitbaibai
RUN apk --no-cache add musl-dev linux-headers g++
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
