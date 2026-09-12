import math
import struct
import wave
import random

SAMPLE_RATE = 44100
MAX_AMP = 32767

def write_wav(filename, samples):
    with wave.open(filename, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SAMPLE_RATE)
        for s in samples:
            v = int(max(-1.0, min(1.0, s)) * MAX_AMP)
            f.writeframesraw(struct.pack('<h', v))

def generate_shoot():
    duration = 0.15
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 1000 * math.exp(t / duration * math.log(100/1000))
        phase += freq / SAMPLE_RATE
        val = math.sin(2 * math.pi * phase) + (random.uniform(-0.5, 0.5) * (1 - t/duration))
        gain = 0.6 * math.exp(t / duration * math.log(0.01/0.6))
        samples.append(val * gain)
    write_wav("audio/shoot.wav", samples)

generate_shoot()
print("shoot.wav generated.")
