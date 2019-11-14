import tkinter as tk

class Menubar(tk.Frame):
    
    def __init__(self, parent):
        pass

    def about_us(self):
        info = (
            "Cyfrowe Przetwarzani Sygnałów.\n"
            "Uniwerystet Kardynała Stefana Wyszyńskiego w Warszawie 2019\n"
            "Autor: Konrad Tarnowski"
            )
        tk.messagebox.showinfo("System analizy dźwięków z sonogramem", info)

    def about_versions(self):
        info = (
            "Python 3.7.2\n")
            # "Tkinter " + str(tkinter.TkVersion) + "\n"
            # "ScyPy " + str(scipy.__version__) + "\n"
            # "NumPy "+ str(np.version.version) + "\n"
            # "MatPlotLib " + str(matplotlib.__version__) + "\n"
            # "PyGame " + str(pygame.version.ver) + "\n"
            # "PILLOW " + str(VERSION) + "\n"
        tk.messagebox.showinfo("System analizy dźwięków z sonogramem", info)