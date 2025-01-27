FROM nvcr.io/nvidia/l4t-base:r36.2.0

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt -y upgrade

# nvcr.io/nvidia/l4t-base:r36.2.0 \

RUN apt install -y --no-install-recommends python3-pip \
         python3-numpy \
         python3-opencv \
         python3-pillow \
         libopencv-dev \
         gstreamer1.0-tools \
         gstreamer1.0-plugins-base \ 
         gstreamer1.0-plugins-good \
         gstreamer1.0-plugins-bad \
         gstreamer1.0-plugins-ugly \
         gstreamer1.0-libav \
         python3-gi \
         gir1.2-gstreamer-1.0 \
         gir1.2-gst-plugins-base-1.0 \
     && apt-get clean \
     && apt-get autoremove \
     && rm -rf /var/cache/apt/archives/* \
     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN mkdir imgs

COPY camera.py test.py test.jpg req.txt /app/

EXPOSE 9000

CMD ["python3", "/app/camera.py"]