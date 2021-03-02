FROM python:3.7-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r src/resources/requirements.txt
EXPOSE 9000
CMD git pull && python start.py