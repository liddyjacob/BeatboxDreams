"""recorder.py
Record an audio file
Borrowed some code from https://gist.github.com/mabdrabo/8678538
"""
import  pyaudio
import wave
from subprocess import Popen
import librosa
import os

""" Record device and return proper librosa objects """
def record(device):

    command = "arecord .temp.wav --device=\"{0}\" > /dev/null".format(device)
    proc = Popen(command, shell=True) # Kill proccess when done
    input("Recording audio, press enter when you are done...")
    proc.kill()

    y, sr = librosa.load(".temp.wav")
    os.remove(".temp.wav")

    return y, sr
