import time
import pyo
import configparser
import jackserver

def start_pyo_server():
    """Start the Pyo server
    
    Return the pyo instance of the server
    """
    pyo_server = pyo.Server(audio='jack', nchnls=1).boot()
    #pyo_server.setJackAuto( False, False )
    pyo_server.start()
    return pyo_server


def chain_effects( initial_source, config_effects_dict ):

    enabled_effects = [initial_source]

    for effect in config_effects_dict.keys():

        source = enabled_effects[len(enabled_effects) - 1]

        # print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
        params = config_effects_dict[effect]
        if effect == 'distortion':
            # distortion stuff
            print("Enable distortion effect")
            enabled_effects.append(pyo.Disto(
                source,
                drive=float(params['drive']),
                slope=float(params['slope']),
                mul=1,
                add=0)
            )

        elif effect == 'delay':
            # delay stuff
            print("Enable delay effect")
            enabled_effects.append(pyo.Delay(
                source,
                delay=[0, float(params['delay'])],
                feedback=float(params['feedback']),
                maxdelay=10,
                mul=1,
                add=0)
            )

        elif effect == 'reverb':
            # reverb stuff
            print("Enable reverb effect")
            enabled_effects.append(pyo.STRev(
                source,
                inpos=0.25,
                revtime=float(params['revtime']),
                cutoff=float(params['cutoff']),
                bal=float(params['balance']),
                roomSize=float(params['roomsize']),
                mul=1,
                add=0)
            )

        elif effect == 'chorus':
            # chorus stuff
            print("Enable chorus effect")
            enabled_effects.append(pyo.Chorus(
                source,
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
            # frequency shift stuff
            print("Enable frequency shift effect")
            enabled_effects.append(pyo.FreqShift(
                source,
                shift=params['shift'],
                mul=1,
                add=0)
            )

        elif effect == 'harmonizer':
            # harmonizer stuff
            print("Enable harmonizer effect")
            enabled_effects.append(pyo.Harmonizer(
                source,
                transpo=params['transpose'],
                feedback=float(params['feedback']),
                winsize=0.1,
                mul=1,
                add=0)
            )

    return enabled_effects


def apply_effects( effects_list ):
    effects_list[len(effects_list) - 1].out()


def main():

    #jackserver.start_jack_server(2, 1)

    pyo_server = start_pyo_server()
    pyo_server.setJackAuto()

    # Read input from the audio device on channel 1
    enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())

    apply_effects( enabled_effects )


    # Eliminate need for GUI with loop - eventually to be used for updating effects.
    # Will be the location of the socket that will establish connection with GUI
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()