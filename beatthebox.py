#!/usr/bin/python3
"""
BeatTheBox

Usage:
    BeatTheBox new <name> [--advanced]
    BeatTheBox load <name>
    BeatTheBox -h | --help

Options:
    -h --help   Show this screen
    --advanced  Make a bigger drumset.
"""
from docopt import docopt
import os
import shutil
import drumtools

def main(arguments):
    name = 'drumsets/' + arguments['<name>']
    if arguments['new']:
        if os.path.isdir(name):
            choice = input("Are you sure you want to overwrite {0}?(y/N): ".format(name))
            if choice != 'y':
                return 0
            else:
                shutil.rmtree(name)

        os.mkdir(name)
        drumtools.setUpDrumset(name)

    # Select drumset
    drumset = drumtools.Drumset(name)

    choice = input("Drumset selected, are YOU ready to make a BEAT?(Y/n): ")
    if choice == 'n':
        return 0

    # record the drums

    print("Great job! now lets make this beat rock more...")

    # Analyze the drums

    no_choice = input("Press enter to hear the revised beat:")


    choice = input("Save the beat?(Y/n): ")
    if choice == 'n':
        return 0

    name = None
    while name is None:
        name = input("Name the beat: ")
        name += ".wav"
        if os.path.exists(name):
            choice = input("Are you sure you want to overwrite {0}.wav?(y/N): ".format(name))
            if choice == 'n' or choice == 'N':
                name = None

    # Save the beat as a wav file.

if __name__ == '__main__':
    ARGS = docopt(__doc__, version='1.0')
    r = main(ARGS)
    print("=== BEAT THE BOX HAS ENDED ===")