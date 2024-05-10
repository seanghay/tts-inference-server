FROM pytorch/pytorch

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

COPY . .

RUN wget https://github.com/seanghay/tts-inference-server/releases/download/1.0.0/pretrained_ljs_sim.onnx