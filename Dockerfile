FROM python:3
RUN git clone https://github.com/veox/python3-krakenex krakenex
WORKDIR /krakenex/
RUN python setup.py install
ADD . /bitbaibai
WORKDIR /bitbaibai
RUN pip install -r requirements.txt
CMD ["python", "main.py"]