import tkinter as tk
from pygame import mixer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# from spectrograph.menubar import Menubar
# from spectrograph.statusbar import Statusbar
from spectrograph.waveplot import WavePlot
from spectrograph.spectrumplot import SpectrumPlot

class MainApplication(tk.Tk):
    """Main class of application"""

    def __init__(self):
        super().__init__()
        self.configure_gui()
        self.create_widgets()
        mixer.init()            # needs for playing sound

    def configure_gui(self):
        """Setting general configurations of the application."""
        self.title("Spectrum analyzer")
        self.geometry("1200x600")
        self.configure(background="white")
        self.iconbitmap("icons/logo_uksw.ico")
        
    def create_widgets(self):
        """Creating the widgets of the application."""
        self.add_waveplot()
        self.add_spectrogram()        

    def add_waveplot(self):
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.X)
        title_label = tk.Label(frame, text="Wykres fali", font="Times 12 italic bold")
        title_label.pack()
        app = WavePlot(100,100)
        figure = app.plotting()
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def add_spectrogram(self):
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.X)
        title_label = tk.Label(frame, text="Spektogram fali", font="Times 12 italic bold")
        title_label.pack()
        app = SpectrumPlot(100)
        figure = app.plotting()
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)



def main():
    """Function to run mianloop"""
    root = MainApplication()
    root.mainloop()
