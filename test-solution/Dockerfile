FROM ultralytics/ultralytics:latest-jetson-jetpack6

RUN pip install dill

WORKDIR /app

COPY . /app

CMD ["python3", "/app/main.py"]