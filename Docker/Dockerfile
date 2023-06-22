FROM tensorflow/tensorflow

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      git \
      python3-dev \
      python3-pip \
      openmpi-bin \
      libeigen3-dev \
      python3-setuptools 

RUN apt-get update && \
    apt-get install -y \
        redis-server

RUN pip install \
    flask \
    flask-kvsession \
    redis \
    futures \
    gunicorn \
    requests \
    python-magic \
    opencv-contrib-python \
    numpy scipy \
    scikit-learn \
    pillow \
    h5py \
    keras \
    torch \
    pillow \
    torchvision \
    matplotlib
    

WORKDIR /home

ENTRYPOINT ["python", "-u", "app.py"]
