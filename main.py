from view import View
from model import Model

class Controller:
    def __init__(self):

        self.model = Model()
        self.view = View(self)

        self.update_status_label()
        self.update_score_laber()


    def main(self):
        self.view.main()
    

    def on_grid_button_click(self, button):
        self.model.button_clicked(button)
        result = self.model.get_cell(button)

        if self.model.updateBoardFlag:
            self.update_board(int(button/100))
            self.model.updateBoardFlag = False
        
        else:
            self.view._update_button(button, result)
        
        if self.model.updatePlayerBoardFlag:
            self.update_board(0)
            self.model.updatePlayerBoardFlag = False
        
        self.update_status_label()
        self.update_score_laber()


    def update_board(self, whichBoard):
        gridOffset = 0
        # whichBoard is 0 for left board, 1 for right board
        if whichBoard:
            gridOffset = 100
        for i in range(100):
            result = self.model.get_cell(i + gridOffset)
            self.view._update_button(i + gridOffset, result)
    

    def on_reset_button_click(self):
        self.model.start_game()
        self.update_board(0)
        self.update_board(1)

        self.update_status_label()
        self.update_score_laber()
    
    
    def update_status_label(self):
        text = self.model.get_status_text()
        self.view.statusText.set(text)

    
    def update_score_laber(self):
        text = self.model.get_score_text()
        self.view.scoreText.set(text)
    

    def on_mute_button_click(self):
        # This does nothing for now
        self.view._toggle_sound_button()



if __name__ == "__main__":
    controller = Controller()
    controller.main()

