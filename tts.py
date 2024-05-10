import numpy as np
import onnxruntime as rt
from tokenizer import tokenize

_model = rt.InferenceSession("pretrained_ljs_sim.onnx")

def audio_float_to_int16(
  audio: np.ndarray, max_wav_value: float = 32767.0
) -> np.ndarray:
  """Normalize audio and convert to int16 range"""
  audio_norm = audio * (max_wav_value / max(0.01, np.max(np.abs(audio))))
  audio_norm = np.clip(audio_norm, -max_wav_value, max_wav_value)
  audio_norm = audio_norm.astype("int16")
  return audio_norm


def create_input(text):
  input_ids = tokenize(text)
  input_ids = np.array(input_ids, dtype=np.int64)
  input_ids = np.expand_dims(input_ids, axis=0)
  input_lengths = np.array([input_ids.shape[1]], dtype=np.int64)
  scales = np.array(
    [0.667, 1, 0.8],
    dtype=np.float32,
  )

  return {"input": input_ids, "input_lengths": input_lengths, "scales": scales}


def text_to_audio(text: str):
  audio_data = _model.run(None, create_input(text))
  audio_data = audio_data[0].squeeze((0, 1))
  audio_data = audio_float_to_int16(audio_data.squeeze())
  return audio_data
