FROM ultralytics/ultralytics:latest

#ultralytics/ultralytics:latest-arm64

WORKDIR /app

COPY . /app

RUN pip3 install dill

CMD ["python3", "/app/main.py"]
