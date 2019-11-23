import numpy as np
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from spectrograph.plot import Plot

class WavePlot(Plot):
    
    def __init__(self):
        self.__xval = np.zeros(1000)
        self.__yval = [0] * 1000

    def plotting(self):
        """Created a WavePlot Figure instance and return it."""
        figure = Figure(figsize=(4, 2), dpi=100)    # figsize - in inch
        axes = figure.add_subplot(111)
        axes.grid(True)
        axes.axhline()    # line y=0
        axes.set_xlim(left=0)
        axes.plot(self.__xval, self.__yval)
        return figure

    @property
    def xval(self):
        return self.__xval

    @xval.setter
    def xval(self, val):
        """OX, time"""
        self.__xval = val

    @property
    def yval(self):
        return self.__yval

    @yval.setter
    def yval(self, val):
        """OY, signal data"""
        self.__yval = val