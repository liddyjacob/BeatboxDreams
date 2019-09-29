"""analyzer.py
Contains the analyze function.
"""
import drumtools
import recognize
import utils
import numpy

def modify(amp_arr, sr, drumset, hop_length = 512):
    """ This is the main algorithm of this project.
    This algorithm will replace specified noises with
    drums, allowing the user to make the world his drumset.

    GOOD LUCK!
    """

    # First thing is first: Analyze the amp_arr and search
    # for the intentional notes played
    beat_frames = utils.getBeatFrames(amp_array=amp_arr, sample_rate=sr)

    # Now its time to analyse each note against the drumset. We will see
    # what the best fit is for each note. We will keep a record of
    # each drum's set of frames

    # Dictionary of drum frames
    drum_frames = {}
    for frame in beat_frames:
        drum = drumset.analyzeAtFrame(amp_arr, frame)
        drum_frames[frame] = drum

    # Finally its time to make a new amp_arr that will contain the
    # new drum beat. We will need to multiply by the maximum frequencies
    # each frame in order to make dynamics work properly.

    # This is a temporary solution to allow extra space for drums that have
    # long sample. Realisticly we need to add the length of the longest sample
    # on the given drumset
    new_amp_arr = numpy.zeros(2 * len(amp_arr), dtype = numpy.float32)

    for key in drum_frames:
        drum = drum_frames[key]
        drum_amp_arr = drumset.soundOf[drum]
        # Calculate drum frame maximums
        maxAmp = utils.findMaxAmp(amp_arr, key, lookahead = 256)

        # insert the new drum sound
        init = key * hop_length
        temp = numpy.add(new_amp_arr[init : init + len(drum_amp_arr)], drum_amp_arr)
        new_amp_arr[init : init + len(drum_amp_arr)] = temp

        # Normalize the volume
        new_amp_arr[init : init + len(drum_amp_arr)] *= maxAmp

    return new_amp_arr
