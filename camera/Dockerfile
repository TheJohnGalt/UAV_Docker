FROM debian:bookworm

RUN apt update && apt -y upgrade

RUN apt update && apt install -y --no-install-recommends \
         python3-pip \
         x11-apps \
         xauth \
     && apt-get clean \
     && apt-get autoremove \
     && rm -rf /var/cache/apt/archives/* \
     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY * .

RUN pip3 install --break-system-packages --no-cache-dir -r requirements.txt

EXPOSE 9000

COPY camera.py test.py test.jpg /app/


CMD ["python3", "/app/test.py"]
