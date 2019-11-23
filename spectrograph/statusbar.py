import tkinter as tk

class Statusbar(tk.Label):

    def __init__(self, parent, *args, **kwargs):
        tk.Label.__init__(self, parent, *args, **kwargs)
        
