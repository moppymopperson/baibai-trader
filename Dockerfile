FROM continuumio/miniconda3
ADD . /bitbaibai
WORKDIR /bitbaibai
RUN pip install -r pip-requirements.txt
RUN conda install --yes --file conda-requirements.txt 
CMD ["python", "main.py"]