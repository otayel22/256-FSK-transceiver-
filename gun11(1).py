import numpy as np
import pyaudio

def modulate_string(input_string, fs=44100, frequency_shift=100):
    p = pyaudio.PyAudio()
    output_device_index = p.get_default_output_device_info()['index']
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True, output_device_index=output_device_index)

    for char in input_string:
        frequency = 1200 + (ord(char) % 255) * frequency_shift
        duration = 0.024  # Adjust as needed
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        signal = np.sin(2 * np.pi * frequency * t)
        stream.write(signal.astype(np.float32).tobytes())

    stream.stop_stream()
    stream.close()
    p.terminate()
while True:
    input_string = input("Enter a string: ")
    modulate_string(input_string)
