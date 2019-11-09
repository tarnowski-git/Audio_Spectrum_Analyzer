import tkinter as tk


class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self._configure_gui()
        self._create_widgets()

    def _configure_gui(self):
        """Setting general configurations of the application."""
        self.configure(background="white")

        self.master.title("Snake game")
        self.master.geometry("500x500")
        self.master.resizable(False, False)



    def _create_widgets(self):
        """Creating the widgets of the application."""
        
        pass


def main():
    """Function to run mianloop"""
    root = tk.Tk()
    main_app =  MainApplication(root)
    root.mainloop()
