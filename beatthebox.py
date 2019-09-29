#!/usr/bin/python3
"""
BeatTheBox

Usage:
    BeatTheBox new <name> [--drums=<drums>]
    BeatTheBox load <name>
    BeatTheBox -h | --help

Options:
    -h --help   Show this screen
    --advanced  Make a bigger drumset.
    --drums=<drum list> Use specified drums for the new
"""
from docopt import docopt
import json
import os
import shutil
import drumtools
from recorder import record
from analyzer import modify
import librosa
from playback import play

def main(arguments):

    settings = None
    with open('settings.json') as jfile:
        settings = json.load(jfile)


    name = 'drumsets/' + arguments['<name>']
    if arguments['new']:
        if os.path.isdir(name):
            choice = input("Are you sure you want to overwrite {0}?(y/N): ".format(name))
            if choice != 'y':
                return 0
            else:
                shutil.rmtree(name)

        os.mkdir(name)
        drumtools.setUpDrumset(name, settings["record_device"])

    # Select drumset
    drumset = drumtools.Drumset(name)

    choice = input("Drumset selected, are YOU ready to make a BEAT?(Y/n): ")
    if choice == 'n':
        return 0

    # record the drums. May need to import microphone
    amp_arr, sr = record(settings["record_device"])

    print("Great job! now lets make this beat rock more...")

    # Analyze and modify the track
    new_amp_arr = modify(amp_arr, sr, drumset)

    # Save the drums temporary:
    librosa.output.write_wav('.temp.wav', new_amp_arr, sr)

    no_choice = input("Press enter to hear the revised beat")

    play('.temp.wav', settings["playback_device"])

    choice = input("Save the beat?(Y/n): ")
    if choice == 'n':
        return 0

    name = None
    while name is None:
        name = input("Name the beat: ")
        name += ".wav"
        if os.path.exists(name):
            choice = input("Are you sure you want to overwrite {0}?(y/N): ".format(name))
            if choice == 'n' or choice == 'N':
                name = None
                continue
        librosa.output.write_wav(name, new_amp_arr, sr)


    os.remove('.temp.wav')
    # Save the beat as a wav file.

if __name__ == '__main__':
    ARGS = docopt(__doc__, version='1.0')
    r = main(ARGS)
    print("=== BEAT THE BOX HAS ENDED ===")
