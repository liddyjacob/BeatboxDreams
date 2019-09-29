"""playback.py
Play the audio file
"""
from subprocess import Popen
def play(path, device = None):

    command = "aplay {0} -q --device=\"{1}\"".format(path, device)
    proc = Popen(command, shell=True) # Kill proccess when done
    input("Playing audio, press enter to stop audio from playing")
    proc.kill()
