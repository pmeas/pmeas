import pyo
import time
import configparser

import bridge

SOCKET_TIMEOUT = 30 #seconds
BOTHER_TRYING_TO_CONNECT = True

def main():
    # Start the server necessary for Pyo to get audio streams from JACK
    s = pyo.Server(audio='jack', nchnls=1).boot()
    s.start()

    # Read input from the audio device on channel 1
    audioIn = pyo.Input(chnl=0)

    effects_dict = configparser.get_effects()
    for effect in effects_dict.keys():
        #print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
        if effect == 'distortion':
            #distortion stuff
            print("Enable distortion effect")
            distortion = pyo.Disto(audioIn, drive=0.75, slope=0.5, mul=1, add=0).out()
        elif effect == 'delay':
            #delay stuff
            print("Enable delay effect")
            delay = pyo.Delay(audioIn, delay=.25, feedback=0.5, mul=0.5).out()
        elif effect == 'reverb':
            #reverb stuff
            print("Enable reverb effect")
            # there's a TON of reverb effects in Pyo. Gotta find out which one is the right to implement.
            reverb = pyo.Freeverb(audioIn, size=0.5, damp=0.5, bal=0.5, mul=1, add=0).out()
        elif effect == 'chorus':
            #chorus stuff
            print("Enable chorus effect")
            chorus = pyo.Chorus(audioIn, depth=1, feedback=0.25, bal=0.5, mul=1, add=0).out()
        elif effect == 'freqshift':
            #frequency shift stuff
            print("Enable frequency shift effect")
            freqshift = pyo.FreqShift(audioIn, shift=100, mul=1, add=0).out()
        elif effect == 'harmonizer':
            #harmonizer stuff
            print("Enable harmonizer effect")
            harmonizer = pyo.Harmonizer(audioIn, transpo=-7.0, feedback=0, winsize=0.1, mul=1, add=0).out()

    #audioIn.out()

    # Effects have now been loaded from last good configuration
    # and the modulator is ready, so we'll block and await
    # await a new configuration. When one arrives, we'll
    # restart the program
    if BOTHER_TRYING_TO_CONNECT:
        with open(configparser.PATH) as effectsFile:
            jstr = bridge.backend(SOCKET_TIMEOUT)
            while not jstr and BOTHER_TRYING_TO_CONNECT:
                jstr = bridge.backend(SOCKET_TIMEOUT)
                effectsFile.write(jstr)
            main()

if __name__ == '__main__':
    main()
