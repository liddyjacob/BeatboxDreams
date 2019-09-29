"""recorder.py
Record an audio file
Borrowed some code from https://gist.github.com/mabdrabo/8678538
"""
import  pyaudio
import wave
from subprocess import Popen
import librosa
import os
import time
""" Record device and return proper librosa objects """
def record(device):

    command = "arecord .temp.wav -q --device=\"{0}\" > .out.log >/dev/null".format(device)
    proc = Popen(command, shell=True) # Kill proccess when done
    input("Recording audio, press enter when you are done...")
    proc.kill()

    y, sr = librosa.load(".temp.wav")
    os.remove(".temp.wav")

    return y, sr

def countdown(seconds):
    for i in range(0, 3):
        count = 3 - i
        print("{0}...".format(count))
        time.sleep(1)
    print("0!")
