FROM python:3.8

RUN apt-get update && apt-get install \
  build-essential \
  libsndfile1 \
  ffmpeg \
  sox \
  libsox-dev \
  libsox-fmt-mp3 \
  cmake \
  espeak \
  git -y


RUN pip install -U --no-cache-dir pip
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check -r requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check unidecode

COPY . .