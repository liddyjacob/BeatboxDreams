""" utils.py
A collection of utils to recognize drums and stuff.
"""
import librosa
import numpy



def getBeatFrames(amp_array, sample_rate, lookahead = 64, significance = 12.0, hop_length = 512):
    """getBeats
    this function returns the 'beats' it detects.
    it uses lookahead to detect insignificant beats

    minimum throws out all beats that are 1/minimum the amplitude
    """
    onset_frames = librosa.onset.onset_detect(y=amp_array, sr=sample_rate);
    max_amps = findMaxAmps(amp_array, onset_frames, lookahead, hop_length);
    av_amps = sum(max_amps) / len(max_amps)

    beat_frames = []
    for i in range(0, len(onset_frames)):
        if (max_amps[i] > av_amps / significance):
            beat_frames.append(onset_frames[i])

    return beat_frames


def fixAmps(amp_array, multiplier_amps, frames, hop_length = 512):
    """fixAmplitude
    Multiply the amplitudes at locations of mul

    amp_array by fixed_amp[i].
    This will decrease the volumes

    multiplier amps is associated with frames. Each frame in frame
    should be mached with a multiplier in multiplier_amps.
    frame    multiplier
    12          0.5
    28          0.9
    34          0.7
    .           .
    .           .
    .           .
    """
    if len(multiplier_amps) != len(frames):
        raise Exception("error: multiplier amps and frames must be equal!");

    # Match amplitude
    for i in range(0, len(multiplier_amps)):

        multiplier = multiplier_amps[i]

        for amp_index in range(frames[i] * hop_length, frames[i] * hop_length + hop_length - 1):
            amp_array[amp_index] *= multiplier


def findMaxAmps(amp_array, frames, lookahead, hop_length = 512):
    """ Find the maximum amps using the maximum of each frame + lookahead

    frames is a list of ints
    lookahead is an int
    """

    max_amps = []

    for init_frame in frames:
        max_amps.append(findMaxAmp(amp_array, init_frame, lookahead, hop_length))

    return max_amps

def findMaxAmp(amp_array, frame, lookahead, hop_length = 512):
    """ Find the maximum amps using the maximum of each frame + lookahead

    frames is a list of ints
    lookahead is an int
    """

    # Multiply by frame length to determine locaiton of beat.
    frame_start_index = frame * hop_length
    max_amp_index = frame_start_index
    for index in range(frame_start_index, frame_start_index + lookahead):

        if abs(amp_array[max_amp_index]) < abs(amp_array[index]):
            max_amp_index = index

    return abs(amp_array[max_amp_index])
