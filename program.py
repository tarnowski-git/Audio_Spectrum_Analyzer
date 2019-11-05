import tkinter.filedialog
import tkinter.messagebox
from tkinter import *

import matplotlib.pyplot as plot
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk
from pygame import mixer
from scipy import signal
from scipy.io import wavfile


class MyApp(object):

    def __init__(self, parent):

        # ustawienie wstępnych parametrów okna
        parent.configure(background="white")
        parent.minsize(1200, 400)
        parent.title("System analizy dźwięków z sonogramem")
        parent.iconbitmap("icons/logo_uksw.ico")

        # utowrzenie górnego menu i paska ze statusem
        self.initial_menu(parent)

        # utowrzenie przycisków i list rozwijanych
        self.initial_frames(parent)

        # utworzenie wykresów i zainicjalizowanie ich domyślnymi wartościami
        self.initial_plots(parent)

        # inicjalizujemy mixer do odtwarzania dzwięku
        mixer.init()


    def about_us(self):
        info = (
            "Cyfrowe Przetwarzani Sygnałów.\n"
            "Uniwerystet Kardynała Stefana Wyszyńskiego w Warszawie 2019\n"
            "Autor: Konrad Tarnowski"
            )
        tkinter.messagebox.showinfo("System analizy dźwięków z sonogramem", info)


    def about_versions(self):
        info = (
            "Python 3.7.2\n")
            # "Tkinter " + str(tkinter.TkVersion) + "\n"
            # "ScyPy " + str(scipy.__version__) + "\n"
            # "NumPy "+ str(np.version.version) + "\n"
            # "MatPlotLib " + str(matplotlib.__version__) + "\n"
            # "PyGame " + str(pygame.version.ver) + "\n"
            # "PILLOW " + str(VERSION) + "\n"
            
        tkinter.messagebox.showinfo("System analizy dźwięków z sonogramem", info)


    def initial_plots(self, parent):
        # tworzymy wstępny wykres fali dzwiękowej
        x = np.zeros(100)
        x1 = np.zeros((100,2))
        y = [0] * 100
        self.waveform_figure = Figure(figsize=(4, 2), dpi=100)   # figsize - rozmiar wykresu w calach;
        self.waveform_axes = self.waveform_figure.add_subplot(111)
        self.waveform_axes.grid(True)
        # tworzymy cięką linię dla y=0
        self.waveform_axes.axhline()
        # ustalamy minimalną wartość dla x
        self.waveform_axes.set_xlim(xmin=0)
        self.waveform_axes.plot(x,y)

        # tworzymy wstępny wykres spektogramu
        self.spectogram_figure = Figure(figsize=(4, 2), dpi=100)
        self.spectogram_axes = self.spectogram_figure.add_subplot(111)
        self.spectogram_axes.grid(True)
        self.spectogram_axes.specgram(x1, NFFT=256, Fs=2)

        # tworzymy ramkę, w której upakujemy wykres fali dźwiękowej
        self.waveforms_frame = Frame(parent, relief=RAISED, borderwidth=3)
        self.waveforms_frame.pack(fill=X)

        title_label_1 = Label(self.waveforms_frame, text="Wykres fali", font="Times 12 italic bold")
        title_label_1.pack()

        # tworzymy kanwę, do której przekonwertujemy wykres dzwięku z MatPlotLib
        self.waveform_canvas = FigureCanvasTkAgg(self.waveform_figure, master=self.waveforms_frame)
        self.waveform_canvas.draw()
        self.waveform_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # tworzymy ramkę, w której upakujemy wykres spektogramu
        self.spectrums_frame = Frame(parent, relief=RAISED, borderwidth=3)
        self.spectrums_frame.pack(fill=X)

        title_label_2 = Label(self.spectrums_frame, text="Spektogram fali", font="Times 12 italic bold")
        title_label_2.pack()

        # tworzymy kanwę, do której przekonwertujemy wykres spektogramu z MatPlotLib
        self.spectogram_canvas = FigureCanvasTkAgg(self.spectogram_figure, master=self.spectrums_frame)
        self.spectogram_canvas.draw()
        self.spectogram_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=TRUE)


    def initial_menu(self, parent):
        """Funkcja do utworzenie paska menu i paska statusu"""
        self.menubar = Menu(parent)

        # umieszcza menubar jako widoczny element w oknie głównym
        parent.config(menu=self.menubar)

        self.submenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Plik", menu=self.submenu)
        self.submenu.add_command(label="Otworz", command=self.browse_file)
        self.submenu.add_command(label="Zakończ", command=parent.quit)

        self.submenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Pomoc", menu=self.submenu)
        self.submenu.add_command(label="O programie", command=self.about_us)
        self.submenu.add_command(label="Wersje", command=self.about_versions)

        # tworzę pasek statusu na samym dole okna
        self.status_bar = Label(parent,text="Oczekiwanie na plik", relief=SUNKEN, anchor=W )
        self.status_bar.pack(side=BOTTOM, fill=X)


    def initial_frames(self, parent):
        """Funkcja, która układa wygląd okienka"""
        # Zbiór przycisków do ustalania parametrów spektogramu
        self.buttons_frame = Frame(parent, relief=RAISED)
        self.buttons_frame.pack(fill=X)

        # StringVar() - obiekt przechowujący zmiany o aktualnym stringu wymagana w niektórych wigetach TK 
        label_1 = Label(self.buttons_frame, text="Okienkowanie", font="Times 10")
        label_1.grid(row=0, column=0, padx=20)
        windows_List = ["hamming", "triang", "blackman", "hann", "bartlett", "flattop", "bohman", "barthann"]
        self.window_var = StringVar()
        self.window_var.set(windows_List[0])
        self.option_menu_1 = OptionMenu(self.buttons_frame, self.window_var, *windows_List)
        self.option_menu_1.grid(row=1, column=0, padx=0)

        label_2 = Label(self.buttons_frame, text="Długość zakładki (%)", padx=20, pady=10, font="Times 10")
        label_2.grid(row=0, column=1)
        overlap_list = ["10", "20", "30", "40", "50", "60", "70", "80", "90"]
        self.overlap_var = StringVar()
        self.overlap_var.set(overlap_list[0])
        self.option_menu_2 = OptionMenu(self.buttons_frame, self.overlap_var, *overlap_list)
        self.option_menu_2.grid(row=1, column=1, padx= 20)

        label_3 = Label(self.buttons_frame, text="Długość próbki", padx=20, pady=10, font="Times 10")
        label_3.grid(row=0, column=2)
        nfft_list = ["16", "32", "64", "128", "256", "512", "1024", "2048"]
        self.nfft_var = StringVar()
        self.nfft_var.set("256")
        self.option_menu_3 = OptionMenu(self.buttons_frame, self.nfft_var, *nfft_list)
        self.option_menu_3.grid(row=1, column=2, padx= 20)

        self.generate_button = Button(self.buttons_frame, text="Generuj wykresy", command=self.generate_plots, font="Times 10 bold")
        self.generate_button.grid(row=0, column=3, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=30, pady=5)

        photo = ImageTk.PhotoImage(Image.open("images/play.png"))
        self.play_button = Button(self.buttons_frame, command=self.play_music, image=photo)
        # muszę zapisać referencję do obrazka, ze względu na Garbage Collector
        self.image_1 = photo
        self.play_button.grid(row=0, column=8, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=10, pady=5)

        photo = ImageTk.PhotoImage(Image.open("images/stop.png"))
        self.stop_button = Button(self.buttons_frame, command=self.stop_music, image=photo)
        # muszę zapisać referencję do obrazka, ze względu na Garbage Collector
        self.image_2 = photo
        self.stop_button.grid(row=0, column=10, columnspan=2, rowspan=2, sticky=W+E+N+S, padx=10, pady=5)


    def browse_file(self):
        """Funkcja, która otwiera plik wave i zapisuje jego ścieżkę."""
        # umożliwiamy wskazać plik .wav użytkownikowi
        ftypes = [("wave files","*.wav")]
        self.filename = tkinter.filedialog.askopenfilename(initialdir="/", filetypes=ftypes, title="Wybierz plik")
        
        # aktualizujemy pasek statusu
        self.status_bar["text"] = "Załadowano plik " + self.filename


    def generate_plots(self):
        # odczytujemy wskazany przez użytkownika plik
        samplingFrequency, signalData = wavfile.read(self.filename)

        # jeśli odczytaliśmy plik dwu kanałowy, to odcinamy ten drugi
        if len(signalData.shape)==2:
            signalData = signalData[:,0]
        
        # obliczamy czas trwania pliku dzwiękowego
        time = np.arange(len(signalData))/float(samplingFrequency)
        
        # aktualizujemy wykres fali dzwiękowej
        self.waveform_axes.clear()
        self.waveform_axes.grid(True)
        # ustalamy minimalną wartość dla x
        self.waveform_axes.set_xlim(xmin=0)
        self.waveform_axes.plot(time, signalData)
        self.waveform_canvas.draw()
        
        # aktualizujemy wykres spektogramu
        self.spectogram_axes.clear()
        self.spectogram_axes.grid(True)
        print(type(signalData))
        # NFFT - długość próbki w okienku (windowing segment/samples in the window)
        # Fs - częstotliwość fali
        # overlap - liczba punktów pokrywających się między segmentami
        overlap_temp=int(self.overlap_var.get())/100
        self.spectogram_axes.specgram(signalData, Fs=samplingFrequency, NFFT=int(self.nfft_var.get()), window=signal.get_window(self.window_var.get(),int(self.nfft_var.get())), noverlap=overlap_temp)
        self.spectogram_canvas.draw()

        
    def play_music(self):
        try:
            print(self.filename)
            mixer.music.load(self.filename)
            mixer.music.play()
        except NameError:
            tkinter.messagebox.showerror("Nie znaleziono pliku", "Program nie mógł znaleźć ścieżki pliku wav. Proszę spróbować ponownie")


    def stop_music(self):
        mixer.music.stop()



# zapobiega wywołaniu poniższego kodu, jeśli ten plik stałby się modułem, a nie programem głównym
if __name__ == "__main__":
    # tworzę główne (podstawowe) okno całej aplikacji (root object)
    root = Tk()
    # tworzę obiekt aplikacji, w którym następuje cała logika programu
    my_app = MyApp(root)
    # niekończona pętla, która utrzymuje okno aplikacji w działaniu
    root.mainloop()
