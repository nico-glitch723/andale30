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
            # clamp
            v = int(max(-1.0, min(1.0, s)) * MAX_AMP)
            f.writeframesraw(struct.pack('<h', v))

def generate_click():
    duration = 0.1
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 440 * math.exp(t / duration * math.log(880/440))
        phase += freq / SAMPLE_RATE
        val = 1.0 if (phase % 1.0) < 0.5 else -1.0
        gain = 0.3 * math.exp(t / duration * math.log(0.01/0.3))
        samples.append(val * gain)
    write_wav("audio/click.wav", samples)

def generate_hit():
    duration = 0.2
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 100 * math.exp(t / duration * math.log(40/100))
        phase += freq / SAMPLE_RATE
        val = 2.0 * (phase % 1.0) - 1.0
        gain = 0.8 * math.exp(t / duration * math.log(0.01/0.8))
        samples.append(val * gain)
    write_wav("audio/hit.wav", samples)

def generate_error():
    duration = 0.3
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 150 * math.exp(t / duration * math.log(120/150))
        phase += freq / SAMPLE_RATE
        val = 2.0 * (phase % 1.0) - 1.0
        gain = 0.6 * math.exp(t / duration * math.log(0.01/0.6))
        samples.append(val * gain)
    write_wav("audio/error.wav", samples)

def generate_success():
    duration = 0.4
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        if t < 0.1: freq = 440
        elif t < 0.2: freq = 554.37
        else: freq = 659.25
        phase += freq / SAMPLE_RATE
        val = math.sin(2 * math.pi * phase)
        gain = 0.4 * math.exp(t / duration * math.log(0.01/0.4))
        samples.append(val * gain)
    write_wav("audio/success.wav", samples)

def generate_groan():
    duration = 1.5
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        freq = 120 - (60 * (t / duration))
        phase += freq / SAMPLE_RATE
        val = 2.0 * (phase % 1.0) - 1.0
        if t < 0.2:
            gain = t / 0.2
        else:
            gain = 1.0 - ((t - 0.2) / 1.3)
        samples.append(val * gain)
    write_wav("audio/groan.wav", samples)

def generate_snore():
    duration = 2.0
    samples = []
    last_val = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        if t < 1.0:
            fc = 100 + 700 * t
            gain = 3.0 * t
        else:
            fc = 800 - 700 * (t - 1.0)
            gain = 3.0 * (2.0 - t)
            
        alpha = (2 * math.pi * fc) / (2 * math.pi * fc + SAMPLE_RATE)
        x = random.uniform(-1.0, 1.0)
        y = alpha * x + (1 - alpha) * last_val
        last_val = y
        samples.append(y * gain)
    write_wav("audio/snore.wav", samples)

def generate_bottle_open():
    duration = 0.15
    samples = []
    last_val_hp = 0.0
    last_x_hp = 0.0
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        
        fc = 3000
        alpha = 1.0 / (1.0 + (2 * math.pi * fc / SAMPLE_RATE))
        x = random.uniform(-1.0, 1.0)
        y_hp = alpha * (last_val_hp + x - last_x_hp)
        last_val_hp = y_hp
        last_x_hp = x
        noise_gain = 2.0 * math.exp(t / 0.15 * math.log(0.01/2.0))
        val = y_hp * noise_gain
        
        if t < 0.05:
            freq = 900 * math.exp(t / 0.05 * math.log(100/900))
            phase += freq / SAMPLE_RATE
            pop_gain = 2.0 * math.exp(t / 0.05 * math.log(0.01/2.0))
            val += math.sin(2 * math.pi * phase) * pop_gain
            
        samples.append(val)
    write_wav("audio/bottle-open.wav", samples)

generate_click()
generate_hit()
generate_error()
generate_success()
generate_groan()
generate_snore()
generate_bottle_open()
print("WAV files generated successfully.")

def generate_heal():
    duration = 0.6
    samples = []
    phase = 0.0
    for i in range(int(SAMPLE_RATE * duration)):
        t = i / SAMPLE_RATE
        if t < 0.2: freq = 440
        elif t < 0.4: freq = 659.25
        else: freq = 880
        phase += freq / SAMPLE_RATE
        val = math.sin(2 * math.pi * phase)
        note_t = t % 0.2
        gain = 0.5 * math.exp(note_t / 0.2 * math.log(0.01/0.5))
        samples.append(val * gain)
    write_wav("audio/heal.wav", samples)

generate_heal()
print("Heal WAV generated.")
