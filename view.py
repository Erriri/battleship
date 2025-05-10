import tkinter as tk
from tkinter import ttk


class View(tk.Tk):


    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.title("Eri's Scuffed Battleship™")
        self.resizable(0, 0)

        self.buttonList = []

        self.statusText = tk.StringVar()
        self.scoreText = tk.StringVar()

        self._make_main_frame()
        self._make_left_grid()
        self._make_right_grid()
        self._make_footer()
    

    def main(self):
        self.mainloop()
    

    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self, width=800, height=600, padding=10)
        self.main_frame.pack()


    def _make_left_grid(self):
        self.leftGrid = ttk.Frame(self.main_frame)
        self.leftGrid.pack(side='left', anchor='nw')
        self._populate_grid(self.leftGrid)


    def _make_right_grid(self):
        self.rightGrid = ttk.Frame(self.main_frame)
        self.rightGrid.pack(padx=(50, 0), side='right', anchor='nw')
        self._populate_grid(self.rightGrid)

    
    def _make_footer(self):
        self.footer = ttk.Frame(self)
        self.footer.pack(side='bottom', anchor="sw", fill='x', padx=10)


        resetButton = ttk.Button(
            self.footer, text="Reset", width=15,
            command = ( lambda : self.controller.on_reset_button_click() )
        )
        resetButton.pack(side="right", pady=(5, 10))

        self.soundButton = ttk.Button(
            self.footer, text="🔊", width=3,
            command = ( lambda : self.controller.on_mute_button_click())
        )
        self.soundButton.pack(side="right", padx=5, pady=(5, 10))

        scoreLabel = ttk.Label(self.footer, textvariable=self.scoreText)
        scoreLabel.pack(side="right", padx=5, pady=(5, 10))
        
        statusLabel = ttk.Label(self.footer, textvariable=self.statusText)
        statusLabel.pack(side="left", pady=(5, 10))


    def _populate_grid(self, Grid):
        
        ## A bit scuffed, but it is probably better than duplicating this function and the list
        gridOffset = 0
        if Grid != self.leftGrid:
            gridOffset = 100

        for i in range (100):
            button = ttk.Button(
                Grid, width=3,
                text=" ",
                command = (lambda c=i+gridOffset: self.controller.on_grid_button_click(c))
            )
            button.grid(row=int(i/10), column=int(i%10))

            self.buttonList.append(button)


    def _update_button(self, buttonID, char):
        self.buttonList[buttonID]["text"] = char
    

    def _toggle_sound_button(self):
        if self.soundButton["text"] == "🔊":
            self.soundButton["text"] = "🔈"
        else:
            self.soundButton["text"] = "🔊"

