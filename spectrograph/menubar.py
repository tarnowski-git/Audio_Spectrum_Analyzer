import tkinter as tk
import tkinter.filedialog

class Menubar(tk.Menu):
    """Create a functional menubar in application."""

    def __init__(self, parent):
        # Create a menubar object
        super().__init__(parent)
        self.parent = parent
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
        self.__filename = None

    def choose_file(self):
        """Only choosing wave files by user and saving its path to `filename`.
        It is not loading the file into program.
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
        info = ("Cyfrowe Przetwarzani Sygnałów.\n"
                "Uniwerystet Kardynała Stefana Wyszyńskiego w Warszawie 2019\n"
                "Autor: Konrad Tarnowski")
        tk.messagebox.showinfo("System analizy dźwięków z sonogramem", info)

    def about_versions(self):
        info = ("Python 3.7.2\n")
            # "Tkinter " + str(tkinter.TkVersion) + "\n"
            # "ScyPy " + str(scipy.__version__) + "\n"
            # "NumPy "+ str(np.version.version) + "\n"
            # "MatPlotLib " + str(matplotlib.__version__) + "\n"
            # "PyGame " + str(pygame.version.ver) + "\n"
            # "PILLOW " + str(VERSION) + "\n"
        tk.messagebox.showinfo("System analizy dźwięków z sonogramem", info)

    @property
    def filename(self):
        """Getter of `filename`"""
        if (self.__filename is not None):
            return self.__filename
        else:
            raise NameError
        