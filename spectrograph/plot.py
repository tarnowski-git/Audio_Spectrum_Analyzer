import numpy as np
from abc import ABC, abstractmethod
from matplotlib.figure import Figure

class Plot(ABC):
    """Abstract class of all plots. Classes derived from this class cannot
    then be instantiated unless all abstract methods have been overridden.
    """
    @abstractmethod
    def plotting(self):
        """Created a Figure instance and return it."""
        return
    
    # @abstractmethod
    # def __generate_plot(self):
    #     pass