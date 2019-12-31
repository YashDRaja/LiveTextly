import tkinter as tk
from tkinter import ttk

#This class was obtained from stackoverflow by users Henry Yik and Tarqez

class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        yscrollbar = tk.Scrollbar(frame, width=width-5)#Changed from stackoverflow
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)#Changed from stackoverflow

        xscrollbar = tk.Scrollbar(frame, width=width-5,orient=tk.HORIZONTAL)#Original Lines
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)#Original Lines

        self.canvas = tk.Canvas(frame, yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)#Xscroll is original
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        xscrollbar.config(command=self.canvas.xview)#Original
        yscrollbar.config(command=self.canvas.yview)#Changed from stack overflow

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))