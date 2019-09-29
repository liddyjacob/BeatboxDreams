"""drumtools.py
A set of functions for setting up
and maintaining the drumset class
The drumset class is located inside of here.
"""
import os
import json
import librosa
from recorder import record
from recorder import countdown
import utils
import recognize
import statistics

class Drumset:
    def __init__(self, name):
        self.path = name
        self.soundOf = {}
        self.drums = []
        self.propertiesOf = {}
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
        self.drums.append(drum)
        # Save the properties for later.
        # Useful in analyzeAtFrame
        self.propertiesOf[drum] = properties
        filename = 'drumsets/sounds/' + properties["audio_file"]
        arr_amp, sr = librosa.load(filename)
        self.soundOf[drum] = arr_amp


    def analyzeAtFrame(self, arr_amp, frame):
        values = {}
        values["freq"] = recognize.avgFreq(arr_amp[frame * 512: (frame + 2) * 512 - 1])
        values["diss"] = recognize.dissipation(arr_amp[frame * 512: frame * 512 + 511])
        values["hv"] = recognize.hillsAndValleys(arr_amp[frame * 512: frame * 512 + 511])
        values["curve"] = recognize.curvature(arr_amp[frame * 512: frame * 512 + 511])

        min_offset = 10000000000000000000000.0
        min_drum = None
        for drum in self.drums:
            properties = self.propertiesOf[drum]
            sum_offset = 0;
            for key in properties["stdevs"]:
                mean = properties["means"][key]
                stdev = properties["stdevs"][key]
                val = values[key]
                # Calculate the offset of the stdev
                offset = abs(mean - val) / stdev
                #Dont know if this is the best way to do this, but...
                sum_offset += offset

            # Find the minimum offsetting drum
            if min_offset > sum_offset:
                min_drum = drum
                min_offset = sum_offset

        return min_drum

""" Make a new folder for the drumset class to read """
def setUpDrumset(name, record_device, drums = ['bass', 'snare']):

    for drum in drums:
        # json properties
        properties = {}
        input("Press enter to record the {0}...".format(drum))
        countdown(3)

        # record the drums. May need to import microphone
        arr_amp, sr = record(record_device)

        beat_frames = utils.getBeatFrames(amp_array=arr_amp, sample_rate=sr, lookahead=256, significance = 7.0)
        beats = librosa.frames_to_time(beat_frames)
        freq_list = []
        diss_list = []
        hv_list = []
        curve_list = []

        # Get the lists
        for frame in beat_frames:
            freq_list.append(recognize.avgFreq(arr_amp[frame * 512: (frame + 2) * 512 - 1]))
            diss_list.append(recognize.dissipation(arr_amp[frame * 512: frame * 512 + 511]))
            hv_list.append(recognize.hillsAndValleys(arr_amp[frame * 512: frame * 512 + 511]))
            curve_list.append(recognize.curvature(arr_amp[frame * 512: frame * 512 + 511]))

        # Get the deviations
        stdev_freq = statistics.stdev(freq_list)
        stdev_diss = statistics.stdev(diss_list)
        stdev_hv = statistics.stdev(hv_list)
        stdev_curve = statistics.stdev(curve_list)

        # averages....
        av_freq = statistics.mean(freq_list)
        av_diss = statistics.mean(diss_list)
        av_hv = statistics.mean(hv_list)
        av_curve = statistics.mean(curve_list)

        properties["stdevs"] = {"freq": stdev_freq,
                                "diss": stdev_diss,
                                "hv": stdev_hv,
                                "curve": stdev_curve}

        properties["means"] = {"freq": av_freq,
                                  "diss": av_diss,
                                  "hv": av_hv,
                                  "curve": av_curve}

        properties["drum_name"] = drum

        # get sound desired
        properties["audio_file"] = input("Audio file name:")

        if properties["audio_file"] is "":
            properties["audio_file"] = drum + '.wav'

        with open(name + '/' + drum + '.json', 'w') as outfile:
            json.dump(properties, outfile)
