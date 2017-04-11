# Portable Multi-Effects Audio Software - *Backend*

## Description
The goal of this project was to create a multi-effects pedal, which can be used by a guitar, but any instrument, including microphone, will also work as well.

As far are effect emulation goes, we rely upon the Pyo Python library to implement 7 supported effects.

* [ Distortion](http://ajaxsoundstudio.com/pyodoc/api/classes/effects.html#disto)
* [ Delay ]( http://ajaxsoundstudio.com/pyodoc/api/classes/effects.html#delay )
* [ Chorus ](http://ajaxsoundstudio.com/pyodoc/api/classes/effects.html#chorus)
* [ Reverb ]( http://ajaxsoundstudio.com/pyodoc/api/classes/effects.html#strev )
* [ Flanger ]( http://ajaxsoundstudio.com/pyodoc/tutorials/pyoobject2.html )
* [ Harmonizer]( http://ajaxsoundstudio.com/pyodoc/api/classes/effects.html#harmonizer )
* [ Frequency Shift ]( http://ajaxsoundstudio.com/pyodoc/api/classes/effects.html#freqshift )

We have also emulated a guitar looper by supporting the Pyo [Looper](http://ajaxsoundstudio.com/pyodoc/api/classes/tableprocess.html#looper) class, which implements a multi-track looper through the help of a optional GPIO button.

## Supported Operating Systems
This backend application is designed to be run on an embedded device, but can also be ran on the same device as the [frontend](https://github.com/pmeas/pmeas-frontend).

Through the help of Python, we are able to support all Linux based distrbutions, as well as all operating systems that support the JACK audio server, even though we only focused exclusively on supporting the Raspberry Pi.

## Necessary Dependencies
* [Python 2.7.13]( https://www.python.org/downloads/ )
* [Pyo 0.7.3]( http://ajaxsoundstudio.com/software/pyo/ )
* [JACK Audio]( http://www.jackaudio.org/ )

## Optional Dependencies
* [Raspberry Pi with Wifi ]( https://www.raspberrypi.org/products/raspberry-pi-3-model-b/ )
  * [Raspbian Jesse](https://www.raspberrypi.org/downloads/raspbian/)
  * Any GPIO Button

## Usage
1. Once all of the **Necessary Dependencies** have been installed, download this repository.
2. Open up your favorite terminal.
3. Change to the project directory, by called `cd <REPOSITORY_NAME>`; replacing `REPOSITORY_NAME` with the name of your downloaded folder.
4. Run `python .` in your terminal.

## Common Issues
* [Application crash](https://github.com/pmeas/pmeas-backend/issues/64)

## Systemd Integration
