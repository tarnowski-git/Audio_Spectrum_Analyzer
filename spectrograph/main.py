import tkinter as tk
import numpy as np
from scipy import signal
from scipy.io import wavfile
from pygame import mixer
from PIL import Image, ImageTk

from spectrograph.plots import WavePlot, SpectrumPlot



class Menubar(tk.Menu):
    """Create a functional menubar in application."""

    INFO = (
        "Digital Processing of Signal\n"
        "Cardinal Stefan Wyszynski University in Warsaw\n"
        "Author: Konrad Tarnowski © 2020"
    )

    def __init__(self, parent):
        # create a menubar object
        super().__init__(parent)
        self.parent = parent
        self.__filename = None

        # Build a file options
        fileMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        fileMenu.add_command(label="Open", command=self.choose_file)
        fileMenu.add_command(label="Exit", command=self.exit)

        # Build a help options
        helpMenu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help",underline=0, menu=helpMenu)
        helpMenu.add_command(label="About", command=self.about)
        helpMenu.add_command(label="Version", command=self.about_versions)
        
    def choose_file(self):
        """Choosing only wave files and saving its path to `filename`.
        """
        # filter to only one type files
        ftypes = [("wave files","*.wav")]
        self.__filename = tk.filedialog.askopenfilename(initialdir="/", filetypes=ftypes, title="Open file")
        
    def exit(self):
        """Closing the program"""
        self.parent.quit()      # stops mainloop
        self.parent.destroy()   # this is necessary on Windows to prevent
                                # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def about(self):                
        tk.messagebox.showinfo("Audio Spectrum Analyzer", self.INFO)

    def about_versions(self):
        info = ("Python 3.7.2\n")
        tk.messagebox.showinfo("Audio Spectrum Analyzer", info)

    @property
    def filename(self):
        """Getter of `filename`"""
        if (self.__filename is not None):
            return self.__filename
        else:
            raise NameError


class Statusbar(tk.Label):

    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)


class Main_Application(tk.Frame):
    """Main class of application"""

    WINDOWING = ["hamming", "triang", "blackman", "hann", "bartlett", "flattop", "bohman", "barthann"]
    OVERLAP = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
    NFFT = ["16", "32", "64", "128", "256", "512", "1024", "2048"]

    IMG_PLAY = "assets/play.png"
    IMG_STOP = "assets/stop.png"

    LARGE_FONT = ("Arial", "14", "bold italic")
    SMALL_FONT = ("Arial", "12")


    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure_gui()
        self.create_widgets()
        self.setup_layout()
        # needs for playing sound
        mixer.init()

    def configure_gui(self):
        """Setting general configurations of the application
        """
        self.master.title("Audio Spectrum Analyzer")
        # +0+0 top left corner on the screen
        # self.master.geometry("1200x600+0+0")
        self.master.configure(background="white")
        self.master.iconbitmap("icons/logo_uksw.ico")
        self.master.resizable(0, 0)
        
    def create_widgets(self):
        """Creating the widgets of the application"""
        # create a Menubar
        self.menubar = Menubar(self)
        # create a subframe for new buttons
        self.frame_buttons = tk.Frame(self.master, bg="white", borderwidth=1, relief="raised")
        # create buttons
        self.add_buttons()
        # create a subframe for plots
        self.frame_plot = tk.Frame(self.master, bg="white")
        # create waveform and spectrgram
        self.add_plots()
        # create a Statusbar
        self.add_statusbar()

    def add_buttons(self):
        # windowing
        self.var_windowing = tk.StringVar()
        self.var_windowing.set(self.WINDOWING[0])
        self.label_windowing = tk.Label(self.frame_buttons, text="Okienkowanie", padx=20, pady=10, font=self.SMALL_FONT, bg="white")
        self.options_windowing = tk.OptionMenu(self.frame_buttons, self.var_windowing, *self.WINDOWING)
        # overlap
        self.var_overlap = tk.StringVar()
        self.var_overlap.set(self.OVERLAP[0])
        self.label_overlap = tk.Label(self.frame_buttons, text="Długość zakładki (%)", padx=20, pady=10, font=self.SMALL_FONT, bg="white")
        self.options_overlap = tk.OptionMenu(self.frame_buttons, self.var_overlap, *self.OVERLAP)
        # nfft
        self.var_nfft = tk.StringVar()
        self.var_nfft.set(self.NFFT[4])
        self.label_nfft = tk.Label(self.frame_buttons, text="Długość próbki", padx=20, pady=10, font=self.SMALL_FONT, bg="white")
        self.options_nfft = tk.OptionMenu(self.frame_buttons, self.var_nfft, *self.NFFT)
        # generate button
        self.button_generate = tk.Button(self.frame_buttons, text="Generate plots", command=self.generate_plots, font=("Arial", "14", "bold"), bg="red", fg="white")
        # play button
        self.image_1 = ImageTk.PhotoImage(Image.open(self.IMG_PLAY))
        self.button_play = tk.Button(self.frame_buttons, command=self.play_sound, image=self.image_1, bg="white")
        # stop button
        self.image_2 = ImageTk.PhotoImage(Image.open(self.IMG_STOP))
        self.button_stop = tk.Button(self.frame_buttons, command=self.stop_sound, image=self.image_2, bg="white")
        # empty buttons - for make a space
        self.space_button_1 = tk.Button(self.frame_buttons, state=tk.DISABLED, relief=tk.FLAT, bg="white")
        self.space_button_2 = tk.Button(self.frame_buttons, state=tk.DISABLED, relief=tk.FLAT, bg="white")

    def add_plots(self):
        self.title_waveform = tk.Label(self.frame_plot, text="Wykres fali", font=self.LARGE_FONT)
        self.canvas_wave = WavePlot(self.frame_plot)
        self.title_spectrograph = tk.Label(self.frame_plot, text="Spektogram fali", font=self.LARGE_FONT)
        self.canvas_spectrum = SpectrumPlot(self.frame_plot)

    def add_statusbar(self):
        self.text_status = tk.StringVar()
        self.text_status.set("Waiting for a file")
        self.statusbar = tk.Label(self.master, textvariable=self.text_status, relief=tk.SUNKEN, anchor=tk.W)
        
    def setup_layout(self):
        """Setup grid system"""
        # set a visibility of menubar in UI
        self.master.config(menu=self.menubar)
        # subframs for relative griding
        self.frame_buttons.grid(row=0, sticky=tk.W+tk.E, pady=0)
        self.frame_plot.grid(row=1, sticky=tk.W+tk.E, pady=10)
        # windowing
        self.label_windowing.grid(row=0, column=0, padx=30)
        self.options_windowing.grid(row=1, column=0, padx=0, pady=10)
        # overlap
        self.label_overlap.grid(row=0, column=1, padx=30, pady=0)
        self.options_overlap.grid(row=1, column=1, padx=30, pady=0)
        # nfft
        self.label_nfft.grid(row=0, column=2, padx=30, pady=0)
        self.options_nfft.grid(row=1, column=2, padx=30, pady=0)
        # create a space
        self.space_button_1.grid(row=0, column=3, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=30, pady=10)
        # generate button
        self.button_generate.grid(row=0, column=5, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)
        # create a space
        self.space_button_2.grid(row=0, column=7, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=30, pady=10)
        # play button
        self.button_play.grid(row=0, column=9, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=10, pady=10)
        # stop button
        self.button_stop.grid(row=0, column=11, columnspan=2, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=20, pady=10)
        # wavefotm
        self.title_waveform.grid(row=0, column=0, columnspan=30)
        self.canvas_wave.get_tk_widget().grid(row=1, column=0, columnspan=30)
        # spectograph
        self.title_spectrograph.grid(row=2, column=0)
        self.canvas_spectrum.get_tk_widget().grid(row=3, column=0)
        # Statusbar
        self.statusbar.grid(row=2, sticky=tk.W+tk.E)

    def generate_plots(self):
        """Load a file and generate plots.

        `sample_rate` : int
            samples/sec (fs)
        `samples` : numpy array
            pass
        `times` : ndarray - sec
            pass
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

            # update a waveform
            self.canvas_wave.plotting(xval=times, yval=samples)

            # # create a spectrum
            self.canvas_spectrum.plotting(xval=samples, nfft=self.var_nfft.get(), fs=sample_rate, 
                                        window=signal.get_window(self.var_windowing.get(), int(self.var_nfft.get())), noverlap=self.var_overlap.get(),duration=len(times))
            
        except TypeError as e:
            print(e)
            print(samples)
            print(sample_rate)
            print(self.var_nfft.get())
            print(self.var_windowing.get())
            print(self.var_overlap.get())
        except NameError as E:
            print(E)
            tk.messagebox.showerror("File not found", "The file path is wrong. Please try again.")


    def play_sound(self):
        try:
            mixer.music.load(self.menubar.filename)
            mixer.music.play()
        except NameError:
            tk.messagebox.showerror("File not found", "Propobly the file path is wrong. Please try again.")

    def stop_sound(self):
        mixer.music.stop()


def main():
    root = tk.Tk()
    application = Main_Application(master=root)
    application.mainloop()
