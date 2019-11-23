import tkinter as tk
import numpy as np
from scipy import signal
from scipy.io import wavfile
from pygame import mixer
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from spectrograph.menubar import Menubar
from spectrograph.waveplot import WavePlot
from spectrograph.spectrumplot import SpectrumPlot

class MainApplication(tk.Tk):
    """Main class of application"""

    WINDOWING = ["hamming", "triang", "blackman", "hann", "bartlett", "flattop", "bohman", "barthann"]
    OVERLAP = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
    NFFT = ["16", "32", "64", "128", "256", "512", "1024", "2048"]

    IMG_PLAY = "assets/play.png"
    IMG_STOP = "assets/stop.png"

    LARGE_FONT = ("Times", "12", "bold italic")
    SMALL_FONT = ("Times", "10")

    def __init__(self):
        super().__init__()
        self.configure_gui()
        self.create_widgets()
        mixer.init()            # needs for playing sound

    def configure_gui(self):
        """Setting general configurations of the application"""
        self.title("Spectrum analyzer")
        self.geometry("1200x600")
        self.configure(background="white")
        self.iconbitmap("icons/logo_uksw.ico")
        
    def create_widgets(self):
        """Creating the widgets of the application"""
        self.add_statusbar()
        self.add_menubar()
        self.add_buttons()
        self.add_plots()

    def add_menubar(self):
        self.menubar = Menubar(self)
        self.config(menu=self.menubar)   # set a visibility of menubar in UI

    def add_plots(self):
        # create a subframe and choose the instatnce
        self.frame_plot = tk.Frame(self, relief=tk.RAISED, borderwidth=3)
        self.frame_plot.pack(fill=tk.X)

        title_label = tk.Label(self.frame_plot, text="Wykres fali", font=self.LARGE_FONT)
        title_label.pack()
        self.wave = WavePlot()
        self.figure_wave = self.wave.plotting()
        self.canvas_wave = FigureCanvasTkAgg(self.figure_wave, master=self.frame_plot)
        self.canvas_wave.draw()
        self.canvas_wave.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

        title_label = tk.Label(self.frame_plot, text="Spektogram fali", font=self.LARGE_FONT)
        title_label.pack()
        self.spectrum = SpectrumPlot()
        self.figure_spectrum = self.spectrum.plotting()
        self.canvas_spectrum = FigureCanvasTkAgg(self.figure_spectrum, master=self.frame_plot)
        self.canvas_spectrum.draw()
        self.canvas_spectrum.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)

    def add_statusbar(self):
        self.text_status = tk.StringVar()
        self.text_status.set("Waiting for a file")
        self.statusbar = tk.Label(self, textvariable=self.text_status, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side="bottom", fill="x")

    def add_buttons(self):
        # create a subframe for new buttons
        frame_buttons = tk.Frame(self, relief=tk.RAISED)
        # create describes as labels
        label_windowing = tk.Label(frame_buttons, text="Okienkowanie", font=self.SMALL_FONT)
        label_overlap = tk.Label(frame_buttons, text="Długość zakładki (%)", padx=20, pady=10, font=self.SMALL_FONT)
        label_nfft = tk.Label(frame_buttons, text="Długość próbki", padx=20, pady=10, font=self.SMALL_FONT)
        # define varieble string objects
        self.var_windowing = tk.StringVar()
        self.var_overlap = tk.StringVar()
        self.var_nfft = tk.StringVar()
        # set default values
        self.var_windowing.set(self.WINDOWING[0])
        self.var_overlap.set(self.OVERLAP[0])
        self.var_nfft.set(self.NFFT[4])
        # create option menues
        options_windowing = tk.OptionMenu(frame_buttons, self.var_windowing, *self.WINDOWING)
        options_overlap = tk.OptionMenu(frame_buttons, self.var_overlap, *self.OVERLAP)
        options_nfft = tk.OptionMenu(frame_buttons, self.var_nfft, *self.NFFT)
        
        button_generate = tk.Button(frame_buttons, text="Generate plots", command=self.generate_plots, font=self.SMALL_FONT)
        self.image_1 = ImageTk.PhotoImage(Image.open(self.IMG_PLAY))
        button_play = tk.Button(frame_buttons, command=self.play_sound, image=self.image_1)
        self.image_2 = ImageTk.PhotoImage(Image.open(self.IMG_STOP))
        button_stop = tk.Button(frame_buttons, command=self.stop_sound, image=self.image_2)

        # placing wigets on the screen
        label_windowing.grid(row=0, column=0, padx=20)
        label_overlap.grid(row=0, column=1)
        label_nfft.grid(row=0, column=2)

        button_generate.grid(row=0, column=3, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=30, pady=5)
        button_play.grid(row=0, column=8, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=5)
        button_stop.grid(row=0, column=10, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=5)

        options_windowing.grid(row=1, column=0, padx=0)
        options_overlap.grid(row=1, column=1, padx= 20)
        options_nfft.grid(row=1, column=2, padx= 20)
        frame_buttons.pack(fill=tk.X)

    def generate_plots(self):
        """Load a file and generate plots.

        `sample_rate` : int
            samples/sec (fs)
        `samples` : numpy array

        `times` : ndarray - sec
        """
        try:
            file_name = self.menubar.filename
            if file_name is not None:
                self.text_status.set("File {} is loaded.".format(file_name))
            else:
                raise NameError

            sample_rate, samples = wavfile.read(file_name)
            samples = samples[:,0]      # if two channels, then select only one channel
            signal_duration = len(samples)
            times = np.linspace(0, signal_duration / sample_rate, num=signal_duration)

            # create a wave
            self.wave.xval = times
            self.wave.yval = samples
            # self.figure_wave.clear()
            # self.figure_test = self.wave.plotting()
            # print(self.figure_wave is self.figure_test)
            # self.figure_wave = self.figure_test
            # print(self.figure_wave is self.figure_test)
            
            # self.canvas_wave = FigureCanvasTkAgg(self.figure_wave, master=self.frame_plot)
            self.canvas_wave.draw()
            # self.canvas_wave._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=tk.TRUE)
            # self.canvas_wave.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
            # self.canvas_wave._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
            # # create a spectrum
            # self.spectrum.xval(samples)
            # self.spectrum.fs(sample_rate)
            # self.spectrum.nfft(self.var_nfft.get())
            # self.spectrum.window(self.var_windowing.get(), self.var_nfft.get())
            # self.spectrum.noverlap(self.var_overlap.get())
            # self.figure_spectrum = self.spectrum.plotting()
            # self.canvas_spectrum.draw()
            # self.canvas_spectrum.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=tk.TRUE)
            
        except TypeError as e:
            print(e)
            print(samples)
            print(sample_rate)
            print(self.var_nfft.get())
            print(self.var_windowing.get())
            print(self.var_overlap.get())
        except NameError as E:
            print(E)
            tk.messagebox.showerror("File not found", "Propobly the file path is wrong. Please try again.")

    def play_sound(self):
        try:
            mixer.music.load(self.menubar.filename)
            mixer.music.play()
        except NameError:
            tk.messagebox.showerror("File not found", "Propobly the file path is wrong. Please try again.")

    def stop_sound(self):
        mixer.music.stop()


def main():
    """run mianloop"""
    root = MainApplication()
    root.mainloop()
