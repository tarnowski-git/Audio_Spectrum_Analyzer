import numpy as np
from scipy import signal
from matplotlib.figure import Figure
from spectrograph.plot import Plot

class SetterProperty(object):
    """A setter descriptor as decorator"""
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


class SpectrumPlot(Plot):
    """Compute and plot a spectrogram of data in `xval`.
    Data are split into NFFT length segments and 
    the spectrum of each section is computed.

    Parameters
    ----------
    `xval` : 1-D array or sequence
        Array containing wave samples.
    `nfft` : int
        The number of data points used in each block for the FFT. A power 2 is most efficient.
    `fs` : scalar
        The sampling frequency (samples per time unit). 
        It is used to calculate the Fourier frequencies,
        freqs, in cycles per time unit.
    `window` : ndarray
        A function or a vector of length NFFT.
    `noverlap` : int
        The number of points of overlap between blocks.
    """

    def __init__(self, xval=[0]*1024):
        self.__xval = xval
        self.__nfft = 256
        self.__fs = 2
        self.__window = np.hamming(self.__nfft)
        self.__noverlap = 128

    def plotting(self):
        """Created a SpectrumPlot Figure instance and return it."""
        figure = Figure(figsize=(4, 2), dpi=100)    # figsize - in inch
        self.axes = figure.add_subplot(111)
        self.axes.clear()
        self.axes.grid(True)
        self.axes.specgram(self.__xval, NFFT=self.__nfft, Fs=self.__fs, window=self.__window, noverlap=self.__noverlap)
        return figure

    @SetterProperty
    def xval(self, val):
        self.__xval = int(val)
    
    @SetterProperty
    def nfft(self, val):
        self.__nfft = int(val)

    @SetterProperty
    def fs(self, val):
        self.__fs = int(val)
    
    @SetterProperty
    def window(self, val1, val2):
        self.__window = signal.get_window(str(val1), int(val2))

    @SetterProperty
    def noverlap(self, val):
        self.__noverlap = int(val) / 100