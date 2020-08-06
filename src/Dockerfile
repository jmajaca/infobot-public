FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install -r resources/requirements.txt
EXPOSE 9000
CMD python main/main.py