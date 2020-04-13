import tkinter as tk

from tkinter.font import Font
from tkinter.ttk import Combobox

from string import ascii_uppercase


class Parking_Gui(tk.Frame):

    PARKING_LOTS = ('ARTX', 'BURG', 'CLAY_HALL', 'GLAB', 'HAMH_HUTC',
                    'HHPA', 'JVIC', 'LIBR', 'PLSU', 'POST', 'PROF',
                    'STEC', 'STRO_NORTH', 'STRO_WEST', 'TROP')

    def __init__(self):
        ...
        self._LotCombo['values'] = Parking_Gui.PARKING_LOTS
        ...

    ...
    def findInBox(self, event):
        keypress = event.char.upper()

        if keypress in ascii_uppercase:
            for index, lot_name in enumerate(Parking_Gui.PARKING_LOTS):
                if lot_name[0] >= keypress:
                    self._LotCombo.current(index)
                    break