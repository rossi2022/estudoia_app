# gerar_audio.py
import wave
import numpy as np
import os

# Caminho onde será salvo
output_path = "backend/tests/audio_teste.wav"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Parâmetros do áudio
framerate = 44100
duration = 1  # segundos
frequency = 440  # Hz
amplitude = 32767

t = np.linspace(0, duration, int(framerate * duration))
data = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

with wave.open(output_path, "w") as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(framerate)
    f.writeframes(data.tobytes())

print(f"Arquivo gerado em: {output_path}")

