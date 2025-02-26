FROM nvcr.io/nvidia/l4t-base:r36.2.0

#
# Install any utils needed for execution
#
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

#
# Install nvidia-cuda-dev for CUDA developer packages
# Use nvidia-cuda if need CUDA runtime only
#
RUN apt-get update && apt-get install -y --no-install-recommends \
    nvidia-cuda-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

#Update libraries
RUN ldconfig 

#
# Setup environment variables
#
ENV CUDA_HOME="/usr/local/cuda"
ENV PATH="/usr/local/cuda/bin:${PATH}"
ENV LD_LIBRARY_PATH="/usr/local/cuda/lib64:${LD_LIBRARY_PATH}"
