from pyo import *

class Flanger(PyoObject):
    def __init__(self, input, depth=0.5, freq=0.25, feedback=0.5, mul=1, add=0):
        PyoObject.__init__(self)
        self._input = input
        self._depth = depth
        self._freq = freq
        self._feedback = feedback
        self._fader = InputFader(input)
        fader, lmax = convertArgsToLists(self._fader)
        self._modamp = Sig(depth, mul=0.01)
        self._mod = Sine(freq=freq, mul=self._modamp, add=0.01)
        self._dls = Delay(fader, delay=self._mod, feedback=feedback)
        self._flanger = Interp(fader, self._dls, mul=mul, add=add)
        self._base_objs = self._flanger.getBaseObjects()

	
