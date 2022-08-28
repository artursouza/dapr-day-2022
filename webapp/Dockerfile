FROM python:3.10-alpine
WORKDIR /webapp
ADD requirements.txt /webapp
RUN pip install -r requirements.txt
ADD main.py /webapp
EXPOSE 8080
CMD ["python","main.py"]