FROM python:alpine3.7
COPY src /app
WORKDIR /app
RUN pip install -r src/resources/requirements.txt
EXPOSE 9000
CMD python start.py