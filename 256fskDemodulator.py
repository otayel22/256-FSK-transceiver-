import pyaudio
import numpy as np

SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
START_FREQ = 1200
BANDWIDTH = 100
NUM_FSK = 256
CHARACTER_MAP = {i: chr(i) for i in range(256)}

FSK_FREQS = [START_FREQ + i * BANDWIDTH for i in range(NUM_FSK)]

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

def detect_frequency(audio_data, sample_rate=SAMPLE_RATE):
    spectrum = np.fft.fft(audio_data)
    frequencies = np.fft.fftfreq(len(audio_data), 1 / sample_rate)
    max_index = np.argmax(np.abs(spectrum))
    #print(max_index)
    #print(frequencies[max_index])
    if max_index > 50:
        dominant_frequency = frequencies[max_index]
        closest_freq = min(FSK_FREQS, key=lambda x: abs(x - dominant_frequency))
        return closest_freq
    return None

while True:
    data = stream.read(CHUNK_SIZE)
    audio_data = np.frombuffer(data, dtype=np.float32)
    detected_freq = detect_frequency(audio_data)
    
    if detected_freq is not None:
        
        symbol = FSK_FREQS.index(detected_freq)
        #print(str(ord(symbol)))                           
        character = CHARACTER_MAP.get(symbol, '?')
        print((character))
