import subprocess

def start_jack_server(inputport, outputport):
    """
    Start the JACK server.

    Keyword arguments:
    inputport -- the port on which to listen for audio data
    outputport -- the port on which to send audio data to.

    Called ONLY when no existing JACK server is running on the machine.
    """
    process = subprocess.call('jackd -P 70 -d alsa -r 48000 -p 1024 -n 2 -D -C &' + inputport + '-P ' + outputport, shell=True)

def get_input_devices():
    """List the input devices captured by the ALSA interface"""
    process = subprocess.Popen(['arecord', '-l'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out

def get_output_devices():
    """List the output devices captured by the ALSA interface"""
    process = subprocess.Popen(['aplay', '-l'], stdout=subprocess.PIPE)
    out, err = process.communicate()
    return out

def filter_shell_output(data):
    """
    Return only the data that identifies what ports are being used

    data -- the output from the call to either
            aplay or arecord.

    Returns a list of strings corresponding to the used ports
    """
    sound_devices = []
    data_arr = data.split("\n")
    for line in data_arr:
        if 'card' in line:
            sound_devices.append(line)
    return sound_devices


def filter_port_selection(selected_port):
    """
    Filter the port data received from the GUI.

    Will extract the card number and device number to allow
    JACK to identify the port selected and lock them for use.

    selected_port -- The raw data received from the GUI application

    Return the port selected formatted for JACK - hw:card,device
    """
    card_num = selected_port.find('card') + 5
    device_num = selected_port[(selected_port.find('device') + 7): (selected_port.rfind(':'))]
    return "hw:" + str(card_num) + "," + str(device_num)
    #print(str(card_num) + ", " + str(device_num))

