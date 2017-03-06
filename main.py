import time
import pyo
import configparser

import bridge

SOCKET_TIMEOUT = 30 #seconds
BOTHER_TRYING_TO_CONNECT = True

def start_pyo_server():
    """Start the Pyo server
    
    Return the pyo instance of the server
    """
    pyo_server = pyo.Server(audio='jack', nchnls=1).boot()
    pyo_server.start()
    return pyo_server

def main():
    pyo_server = start_pyo_server()

    enabled_effects = []

    # Read input from the audio device on channel 1
    enabled_effects.append(pyo.Input(chnl=0))

    effects_dict = configparser.get_effects()
    for effect in effects_dict.keys():
        #print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
        params = effects_dict[effect]
        if effect == 'distortion':
            #distortion stuff
            print("Enable distortion effect")
            enabled_effects.append(pyo.Disto(
                                    enabled_effects[len(enabled_effects)-1],
                                    drive=float(params['drive']),
                                    slope=float(params['slope']),
                                    mul=1,
                                    add=0)
                                )
        elif effect == 'delay':
            #delay stuff
            print("Enable delay effect")
            enabled_effects.append(pyo.Delay(
                                    enabled_effects[len(enabled_effects)-1],
                                    delay=[0, float(params['delay'])],
                                    feedback=float(params['feedback']),
    				maxdelay=10,
    				mul=1,
                                    add=0)
                                )
        elif effect == 'reverb':
            #reverb stuff
            print("Enable reverb effect")
            enabled_effects.append(pyo.STRev(
                                    enabled_effects[len(enabled_effects)-1],
                                    inpos=0.25,
                                    revtime=float(params['revtime']),
                                    cutoff=float(params['cutoff']),
                                    bal=float(params['balance']),
                                    roomSize=float(params['roomsize']),
    				mul=1,
    				add=0)
                                )
        elif effect == 'chorus':
            #chorus stuff
            print("Enable chorus effect")
            enabled_effects.append(pyo.Chorus(
                                    enabled_effects[len(enabled_effects)-1],
                                    depth=float(params['depth']),
                                    feedback=float(params['feedback']),
                                    bal=float(params['balance']),
                                    mul=1,
                                    add=0)
                                )
    #    This will be used once the class is created
    #
    #    elif effect == 'flanger':
    #        #harmonizer stuff
    #        print("Enable flanger effect")
    #        enabled_effects.append(pyo.Flanger(
    #                                enabled_effects[len(enabled_effects)-1],
    #                                depth=float(params['depth']),
    #                                lfofreq=float(params['lfofreq']),
    #				feedback=float(params['feedback']),
    #                                mul=1,
    #                                add=0)
    #                            )
        elif effect == 'freqshift':
            #frequency shift stuff
            print("Enable frequency shift effect")
            enabled_effects.append(pyo.FreqShift(
                                    enabled_effects[len(enabled_effects)-1],
                                    shift=params['shift'],
                                    mul=1,
                                    add=0)
                                )
        elif effect == 'harmonizer':
            #harmonizer stuff
            print("Enable harmonizer effect")
            enabled_effects.append(pyo.Harmonizer(
                                    enabled_effects[len(enabled_effects)-1],
                                    transpo=params['transpose'],
                                    feedback=float(params['feedback']),
                                    winsize=0.1,
                                    mul=1,
                                    add=0)
                                )

    enabled_effects[len(enabled_effects)-1].out()

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
