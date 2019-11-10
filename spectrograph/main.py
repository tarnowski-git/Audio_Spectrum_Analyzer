import tkinter as tk

class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self._configure_gui()
        self._create_widgets()

    def _configure_gui(self):
        """Setting general configurations of the application."""
        self.master.configure(background="white")
        self.master.title("Spectrum analyzer")
        # self.master.minsize(1200, 400)
        self.master.geometry("1200x400")
        # self.master.resizable(False, False)
        self.master.iconbitmap("icons/logo_uksw.ico")
        
    def _create_widgets(self):
        """Creating the widgets of the application."""
        pass


def main():
    """Function to run mianloop"""
    root = tk.Tk()
    MainApplication(root)
    root.mainloop()
