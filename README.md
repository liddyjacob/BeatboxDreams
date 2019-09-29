# BeatboxDream: A terrible beatboxer's dream.

This program will convert beatbox to real drums
I should rename this to 'the world is your drumset'

## REQUIREMENTS
* install multimedia jack for ubuntu:
```
sudo apt install multimedia-jack
pulseaudio --kill
jack\_control  start
```
* arecord(preintalled on ubuntu 18.04, useful for making .wav files.)

## INSTRUCTIONS
Make sure settings.json has your audio device listed. Use arecord -L to find audio devices.
