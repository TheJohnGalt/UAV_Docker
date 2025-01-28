FROM ultralytics/ultralytics:latest-jetson-jetpack6

RUN pip install dill

WORKDIR /app

COPY benchmark.py best.pt best_fire.pt main.py main_fire.py solution.py /app

RUN mkdir container_output

CMD ["python3", "/app/benchmark.py"]
