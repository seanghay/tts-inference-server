import regex as re
from unidecode import unidecode
from phonemizer import phonemize

_pad = "_"
_punctuation = ';:,.!?¡¿—…"«»“” '
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_letters_ipa = "ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ"

symbols = [_pad] + list(_punctuation) + list(_letters) + list(_letters_ipa)

_symbol_to_id = {s: i for i, s in enumerate(symbols)}
_id_to_symbol = {i: s for i, s in enumerate(symbols)}

_whitespace_re = re.compile(r"\s+")
_abbreviations = [
  (re.compile("\\b%s\\." % x[0], re.IGNORECASE), x[1])
  for x in [
    ("mrs", "misess"),
    ("mr", "mister"),
    ("dr", "doctor"),
    ("st", "saint"),
    ("co", "company"),
    ("jr", "junior"),
    ("maj", "major"),
    ("gen", "general"),
    ("drs", "doctors"),
    ("rev", "reverend"),
    ("lt", "lieutenant"),
    ("hon", "honorable"),
    ("sgt", "sergeant"),
    ("capt", "captain"),
    ("esq", "esquire"),
    ("ltd", "limited"),
    ("col", "colonel"),
    ("ft", "fort"),
  ]
]


def expand_abbreviations(text):
  for regex, replacement in _abbreviations:
    text = re.sub(regex, replacement, text)
  return text


def lowercase(text):
  return text.lower()


def collapse_whitespace(text):
  return re.sub(_whitespace_re, " ", text)


def convert_to_ascii(text):
  return unidecode(text)


def basic_cleaners(text):
  """Basic pipeline that lowercases and collapses whitespace without transliteration."""
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def transliteration_cleaners(text):
  """Pipeline for non-English text that transliterates to ASCII."""
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = collapse_whitespace(text)
  return text


def english_cleaners(text):
  """Pipeline for English text, including abbreviation expansion."""
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_abbreviations(text)
  phonemes = phonemize(text, language="en-us", backend="espeak", strip=True)
  phonemes = collapse_whitespace(phonemes)
  return phonemes


def english_cleaners2(text):
  """Pipeline for English text, including abbreviation expansion. + punctuation + stress"""
  text = convert_to_ascii(text)
  text = lowercase(text)
  text = expand_abbreviations(text)
  phonemes = phonemize(
    text,
    language="en-us",
    backend="espeak",
    strip=True,
    preserve_punctuation=True,
    with_stress=True,
  )
  phonemes = collapse_whitespace(phonemes)
  return phonemes


def text_to_sequence(text):
  sequence = []
  clean_text = english_cleaners2(text)
  for symbol in clean_text:
    symbol_id = _symbol_to_id[symbol]
    sequence += [symbol_id]
  return sequence


def cleaned_text_to_sequence(cleaned_text):
  sequence = [_symbol_to_id[symbol] for symbol in cleaned_text]
  return sequence


def sequence_to_text(sequence):
  """Converts a sequence of IDs back to a string"""
  result = ""
  for symbol_id in sequence:
    s = _id_to_symbol[symbol_id]
    result += s
  return result


def intersperse(lst, item):
  result = [item] * (len(lst) * 2 + 1)
  result[1::2] = lst
  return result


def tokenize(text):
  seq = text_to_sequence(text)
  seq = intersperse(seq, 0)
  return seq
