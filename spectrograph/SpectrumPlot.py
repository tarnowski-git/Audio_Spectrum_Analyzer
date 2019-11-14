import numpy as np
from matplotlib.figure import Figure
from spectrograph.plot import Plot

class SpectrumPlot(Plot):
    
    def __init__(self, xval=None):
        self.xval = np.zeros((xval,2))

    def plotting(self):
        """Created a SpectrumPlot Figure instance and return it."""
        figure = Figure(figsize=(4, 2), dpi=100)    # figsize - in inch
        axes = figure.add_subplot(111)
        axes.grid(True)
        axes.specgram(self.xval, NFFT=256, Fs=2)
        return figure