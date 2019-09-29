"""drumtools.py
A set of functions for setting up
and maintaining the drumset class
The drumset class is located inside of here.
"""
import os
import json
import librosa

class Drumset:
    def __init__(self, name):
        self.path = name
        self.soundOf = {}
        self._setUpComponents()

    def _setUpComponents(self):
        for f in os.listdir(self.path):
            path = self.path + "/" + f
            if path.endswith('.json'):
                self._setUpComponent(path)

    def _setUpComponent(self, path):
        properties = None
        with open(path) as jfile:
            properties = json.load(jfile)

        drum = properties["drum_name"]

        filename = 'drumsets/' + properties["audio_file"]
        arr_amp, sr = librosa.load(filename)
        self.soundOf[drum] = arr_amp


    def analyzeAtFrame(self, arr_amp, frame):
        return "snare"

""" Make a new folder for the drumset class to read """
def setUpDrumset(name):
    pass
