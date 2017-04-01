#!/usr/bin/python

GPIO_CAPABLE = False

import time

import pyo
try:
    import RPi.GPIO as GPIO
    GPIO_CAPABLE = True
except ImportError:
    pass

if GPIO_CAPABLE:
    import gpiocontrol
import bridge
import configparser
import jackserver
import flanger 

import socket

SOCKET_TIMEOUT = 30 #seconds

button_pin = 17


def start_pyo_server():
    """Start the Pyo server
    
    Return the pyo instance of the server
    """
    print("Attempting to start the pyo server")
    pyo_server = pyo.Server(audio='jack', nchnls=1).boot()
    print("Pyo server booted")
    #pyo_server.setJackAuto( False, False )
    pyo_server.start()
    print("Pyo server started")
    return pyo_server


def chain_effects( initial_source, config_effects_dict ):
    main_volume = 1 #default volume 
    enabled_effects = [initial_source]
    for effect in sorted(config_effects_dict.keys()):

        source = enabled_effects[len(enabled_effects) - 1]

        # print("Effect: " + effect + ", Params: " + str(effects_dict[effect]))
        params = config_effects_dict[effect]
        if effect == 'volume':
            # volume stuff
            print("Volume captured")
            main_volume=float(params['vol'])

        elif params['name'] == 'distortion':
            # distortion stuff
            print("Enable distortion effect")
            enabled_effects.append(pyo.Disto(
                source,
                drive=float(params['drive']),
                slope=float(params['slope']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'delay':
            # delay stuff
            print("Enable delay effect")
            enabled_effects.append(pyo.Delay(
                source,
                delay=[0, float(params['delay'])],
                feedback=float(params['feedback']),
                maxdelay=10,
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'reverb':
            # reverb stuff
            print("Enable reverb effect")
            enabled_effects.append(pyo.STRev(
                source,
                inpos=0.25,
                revtime=float(params['revtime']),
                cutoff=float(params['cutoff']),
                bal=float(params['balance']),
                roomSize=float(params['roomsize']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'chorus':
            # chorus stuff
            print("Enable chorus effect")
            enabled_effects.append(pyo.Chorus(
                source,
                depth=float(params['depth']),
                feedback=float(params['feedback']),
                bal=float(params['balance']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'flanger':
            # flanger stuff
            print("Enable flanger effect")
            enabled_effects.append(flanger.Flanger(
                source,
                depth=float(params['depth']),
                freq=float(params['freq']),
                feedback=float(params['feedback']),
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'freqshift':
            # frequency shift stuff
            print("Enable frequency shift effect")
            enabled_effects.append(pyo.FreqShift(
                source,
                shift=params['shift'],
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'harmonizer':
            # harmonizer stuff
            print("Enable harmonizer effect")
            enabled_effects.append(pyo.Harmonizer(
                source,
                transpo=params['transpose'],
                feedback=float(params['feedback']),
                winsize=0.1,
                mul=main_volume,
                add=0)
            )

        elif params['name'] == 'phaser':
            # phaser stuff
            print("Enable phaser effect")
            enabled_effects.append(pyo.Phaser(
                source,
                freq=float(params['frequency']),
                spread=float(params['spread']),
                q=float(params['q']),
                feedback=float(params['feedback']),
                num=int(params['num']),
                mul=main_volume,
                add=0)
            )

    return enabled_effects


def apply_effects( effects_list ):
    effects_list[len(effects_list) - 1].out()

def main():

    # If GPIO is enabled, initialize the pins and GPIO module.
    if GPIO_CAPABLE:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(button_pin, GPIO.IN, GPIO.PUD_UP)

        gpio_controller = gpiocontrol.GpioController()

    bridge_conn = bridge.Bridge()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP SOCKET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP SOCKET
    s.setblocking(0)
    sock.setblocking(0)
    s.bind(('', 10000))
    sock.bind(('', 10001))

    # Add your own input and output ports here for now
    jack_id = jackserver.start_jack_server('3,0', '0,3')

    time.sleep(5)

    # JACK and Pyo set up procedures
    #jackserver.start_jack_server(2, 1)
    pyo_server = start_pyo_server()
    pyo_server.setJackAuto()

    # Read input from the audio device on channel 0
    # and apply the necessary effects from the config file 
    enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())
    apply_effects( enabled_effects )

    # Create necessary variables used by the GPIO controller module
    record_table = []
    audio_recorder = []
    loop = []
    record_table.append(pyo.NewTable(length=60, chnls=1, feedback=0.5))
    audio_recorder.append(pyo.TableRec((enabled_effects[len(enabled_effects) - 1]), table=record_table[-1], fadetime=0.05))
    already_recording = False
    recording_time = 0
    inactive_end_time = 0

    while True:
        # Effects have now been loaded from last good configuration
        # and the modulator is ready, so we'll block and await
        # await a new configuration. When one arrives, we'll
        # restart the program
        # TODO: Check the result of res to see if we should update effects.

        # Executes GPIO and loop machine logic flow.
        # TODO: Transfer flow to another process to simplify main() readability.
        if GPIO_CAPABLE:
            # Read the state of the button press. 
            BUTTON_STATE = gpio_controller.update_gpio()
            # Perform actions dependent on the state of the button press.
            if BUTTON_STATE == 'INACTIVE' or BUTTON_STATE == 'LOOPING':
                inactive_end_time = time.time()
            if BUTTON_STATE == 'RECORDING':
                recording_time = time.time()
                if not already_recording:
                    print("Recording audios for 5 segundos")
                    (audio_recorder[-1]).play()
                    already_recording = True
            elif BUTTON_STATE == 'ACTIVATE_LOOP':
                loop_len = recording_time - inactive_end_time
                loop.append(
                    pyo.Looper(
                        table=record_table[-1],
                        dur=loop_len, xfade=0,
                        mul=1).out()
                    )
                record_table.append(
                    pyo.NewTable(
                        length=60,
                        chnls=1,
                        feedback=0.5)
                    )
                audio_recorder.append(
                    pyo.TableRec(
                        (enabled_effects[len(enabled_effects) - 1]),
                        table=record_table[-1],
                        fadetime=0.05)
                    )
                print("ACTIVATING LOOP")
                gpio_controller.set_state("LOOPING")
                already_recording = False
            elif BUTTON_STATE == 'CLEAR_LOOP':
                loop = []
                record_table = []
                audio_recorder = []
                record_table.append(
                    pyo.NewTable(
                        length=60,
                        chnls=1,
                        feedback=0.5)
                    )
                audio_recorder.append(
                    pyo.TableRec(
                        (enabled_effects[len(enabled_effects) - 1]),
                        table=record_table[-1],
                        fadetime=0.05)
                    )
                gpio_controller.set_state("INACTIVE")

        res = bridge_conn.backend(s,sock)
        if res:
            print(res)
            if 'Updated_ports' in res:
                print("Request to update ports")
                pyo_server.shutdown()
                jackserver.stop_jack_server(jack_id)
                time.sleep(2)
                jackserver.start_jack_server("3,0", "1,0")
                time.sleep(2)
                pyo_server = start_pyo_server()
                enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())
                apply_effects( enabled_effects )
            else:
                enabled_effects = chain_effects(pyo.Input(chnl=0), configparser.get_effects())
                apply_effects(enabled_effects)
        #print(res)
        time.sleep(0.0001)


if __name__ == "__main__":
    main()
