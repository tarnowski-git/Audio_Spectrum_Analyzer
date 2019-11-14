import numpy as np
from matplotlib.figure import Figure
from spectrograph.plot import Plot

class WavePlot(Plot):
    
    def __init__(self, xval=None, yval=None):
        self.xval = np.zeros(xval)
        self.yval = [0] * yval

    def plotting(self):
        """Created a WavePlot Figure instance and return it."""
        figure = Figure(figsize=(4, 2), dpi=100)    # figsize - in inch
        axes = figure.add_subplot(111)
        axes.grid(True)
        axes.axhline()    # line y=0
        axes.set_xlim(xmin=0)
        axes.plot(self.xval, self.yval)
        return figure