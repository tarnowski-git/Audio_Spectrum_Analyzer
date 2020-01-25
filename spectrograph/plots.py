import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import specgram
from scipy import signal


class WavePlot(FigureCanvasTkAgg):
    """Compute and plot a waveform of data in `xval`.

    Parameters
    ----------
    `parent` : master widget
        Represents a widget to act as the parent of the current object
    `xval` : 1-D array or sequence
        The number of data points in timeline.
    `yval` : 1-D array or sequence
        Array containing wave samples.
    """

    def __init__(self, parent=None, xval=np.zeros(1000), yval=[0] * 1000):
        self.__xval = xval
        self.__yval = yval
        figure = Figure(figsize=(4, 2), dpi=100)    # figsize - in inch
        super().__init__(figure, master=parent)
        self.axes = figure.add_subplot(111)
        self.axes.grid(True)
        self.axes.axhline()                         # line y=0
        self.axes.set_xlim(left=0)
        self.axes.plot(self.__xval, self.__yval)
        self.draw()

    def plotting(self, xval, yval):
        """Updating a WavePlot Figure instance and drawing plot."""
        self.__xval = xval
        self.__yval = yval
        self.axes.clear()
        self.axes.grid(True)
        self.axes.axhline()
        self.axes.set_xlim(left=0)
        self.axes.plot(self.__xval, self.__yval)
        self.draw()


class SetterProperty(object):
    """A setter descriptor as decorator"""

    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


class SpectrumPlot(FigureCanvasTkAgg):
    """Compute and plot a spectrogram of data in `xval`.
    Data are split into NFFT length segments and 
    the spectrum of each section is computed.

    Parameters
    ----------
    `parent` : master widget
        Represents a widget to act as the parent of the current object
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

    def __init__(self, parent=None, xval=np.zeros(1000), nfft=256, fs=2, noverlap=900):

        # init variables
        self.__xval = xval
        self.__nfft = 256
        self.__fs = 2
        # self.__window = np.hamming(self.__nfft)
        self.__noverlap = 128

        # create a figure
        figure = Figure(figsize=(4, 2), dpi=100)    # figsize - in inch
        super().__init__(figure, master=parent)
        self.axes = figure.add_subplot(111)
        self.axes.grid(True)
        self.axes.specgram(self.__xval, NFFT=self.__nfft,
                           Fs=self.__fs, noverlap=self.__noverlap)
        self.draw()

    def plotting(self, xval, nfft, fs, window, noverlap, time):
        """Updating a SpectrumPlot Figure instance and drawing plot."""

        self.__xval = xval
        self.__nfft = int(nfft)
        self.__fs = int(fs)
        self.__window = window
        self.__noverlap = int(noverlap) / 100
        self.__time = len(time)

        self.axes.clear()
        self.axes.grid(True)
        self.axes.specgram(self.__xval, NFFT=self.__nfft, Fs=self.__fs,
                           window=self.__window, noverlap=self.__noverlap, xextent=(0, 1))
        self.draw()

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
