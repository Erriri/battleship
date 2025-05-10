from resources.generate_enemy_board import GenerateEnemyBoard
from resources.generic_board_stuff import BoardStuff
from resources.enemy_player import EnemyPlayer

class Model:
    
    def __init__(self):
        self.boardFunctions = BoardStuff()
        self.enemyBoardGenerator = GenerateEnemyBoard()
        self.start_game()



    def start_game(self):
        ### GameState
        ## 0 - player places ships
        # click on enemy grid does nothing
        # click on your grid checks if it is a legal position for ship, and places it if it is
        ## 1 - player shoots
        # clicks on your grid do nothing
        # click on enemy grid to take a shot, unless you tried that cell already
        ## 2 - enemy shoots
        ## 3 - game ended, you won
        ## 4 - game ended, you lost
        self.gameState = 0

        # This flag exists to update more than one cell per button press, only in certain situations
        self.updateBoardFlag = False

        # This flag exists to update specifically the player board after enemy turns
        self.updatePlayerBoardFlag = False

        self.enemyPlayer = EnemyPlayer()

        # Stuff you don't see
        self.enemyBoard = self.enemyBoardGenerator.generate_ships()

        # Stuff you see
        self.playerBoard = self.boardFunctions.make_empty_board(" ")
        self.enemyBoardVisible = self.boardFunctions.make_empty_board(" ")
        

        self.initiate_ship_placement_counters()


    # def get_cell(self, button):
    #     if button > 99:
    #         return self.enemyBoard[button-100]
    #     return self.playerBoard[button]


    def get_cell(self, button):
        if button > 99:
            return self.enemyBoardVisible[button-100]
        return self.playerBoard[button]


    def initiate_ship_placement_counters(self):
        # The size of the ship you should place
        self.shipSize = 4
        # It goes down by 1 after you have placed all ships of that size

        # How many ships of this size you need to place
        self.shipCounterBySize = 1
        # It goes down by 1 after placing a full ship
        # Then it is reset, and the value it is reset to increases by 1
        self.shipNextCounter = 1

        # How many steps do you have left
        self.shipPartCountdown = self.shipSize
        # It goes down by 1 after placing a ship part

        # For borders
        self.currentShipCells = []

        # Place one 4 long ship
        # Place two 3 long ships
        # Place three 2 long ships
        # Place four 1 long ships


    def button_clicked(self, button):
        # " " -> empty cell
        # "O" -> ship cell
        # "X" -> destroyed ship cell
        # "●" -> empty cell that was shot
        # "-" -> functional border for ship cells, is created when a ship is fully sunk to prevent unnecessary shots 
        # "-" -> also a border for ship cells during generation, replaced with " " afterwards
        # "*" -> cells that can be part of a big ship, used for generating bigger ships. Goes in 4 directions, after placing the first cell
        # "+" -> cells that can be part of a big ship, used for generating bigger ships. Only on one axis, after placing the second cell

        match(self.gameState):
            # Ship placing phase
            case 0:
                if button < 100:
                    # You still have ships to place
                    if self.shipSize:

                        # You still have ship parts to place
                        if self.shipPartCountdown:
                            self.place_ship(button, self.playerBoard)
                            ## self.shipPartCountdown--
                    
                    # You have placed a full ship
                    if not self.shipPartCountdown:
                        self.boardFunctions.clear_cell_markings(self.playerBoard, "+")
                        # Place border markers
                        self.boardFunctions.place_border_marks(self.playerBoard, self.currentShipCells, "-")

                        self.currentShipCells = []
                        self.shipCounterBySize -= 1

                        # You have placed all ships of this size
                        if not self.shipCounterBySize:
                            # Lower ship size
                            self.shipSize -= 1
                            # Increase count of ships of new size
                            self.shipNextCounter += 1
                            # Reset counter by ship size
                            self.shipCounterBySize = self.shipNextCounter
                        
                        # Place a new ship
                        self.shipPartCountdown = self.shipSize
                    
                    # You are out of ships to place
                    if not self.shipSize:
                        # Call a function to clean up the ship borders
                        self.boardFunctions.clear_cell_markings(self.playerBoard, "-")

                        # Shooty time
                        self.gameState = 1


            # Your turn to shoot
            case 1:
                if button > 99:
                    self.take_shot(button - 100)
                    if self.boardFunctions.is_game_over(self.enemyBoard):
                        self.gameState = 3
        
        
        # Enemy turn. Do something there
        if self.gameState == 2:
            self.run_enemy_turn()
            if self.boardFunctions.is_game_over(self.playerBoard):
                self.gameState = 4
            
        

    def take_shot(self, button):
        cell = self.enemyBoard[button]
        if cell == "O":
            self.enemyBoard[button] = "X"
            self.enemyBoardVisible[button] = "X"

            if self.boardFunctions.is_ship_sunk(self.enemyBoard, button):
                # Gotta add ship borders
                # self.boardFunctions.shipCells is created by the is_ship_sunk function itself
                self.boardFunctions.place_border_marks(self.enemyBoardVisible, self.boardFunctions.shipCells, "-")
                self.updateBoardFlag = True
        elif cell != "X" and cell != "●":
            self.enemyBoardVisible[button] = "●"
            self.gameState = 2


    def place_ship(self, button, board):
        cell = board[button]
        
        ### If this is the first cell of a big ship, mark 4 neighboring cells with *
        if self.shipPartCountdown == self.shipSize:
            if cell == " ":
                board[button] = "O"
                self.currentShipCells.append(button)

                self.shipPartCountdown -= 1

                self.updateBoardFlag = True
            
                ### No need to do this for 1 sized ships
                if self.shipSize > 1:
                    # left
                    if button % 10 > 0 and board[button - 1] == " ":
                        board[button - 1] = "*"
                    
                    # right
                    if button % 10 < 9 and board[button + 1] == " ":
                        board[button + 1] = "*"

                    # top
                    if button > 9 and board[button - 10] == " ":
                        board[button - 10] = "*"
                    
                    # bottom
                    if button < 90 and board[button + 10] == " ":
                        board[button + 10] = "*"

        ### If this isn't the first cell, replace * with either + or _
        else:
            # This is the second cell
            if cell == "*":
                board[button] = "O"
                self.updateBoardFlag = True
                self.boardFunctions.clear_cell_markings(board, "*")

                self.currentShipCells.append(button)
                self.currentShipCells.sort()

                self.place_pluses(board)

                self.shipPartCountdown -= 1


            # This isn't the second cell
            if cell == "+":
                board[button] = "O"
                self.updateBoardFlag = True

                self.currentShipCells.append(button)
                self.currentShipCells.sort()

                self.place_pluses(board)

                self.shipPartCountdown -= 1


    def place_pluses(self, board):
        lastButton = self.currentShipCells[-1]
        firstButton = self.currentShipCells[0]
        delta = self.currentShipCells[1] - firstButton

        # Check if first position makes sense
        if self.check_next_plus_position(delta, lastButton):
            if board[lastButton + delta] == " ":
                board[lastButton + delta] = "+"

        # Check if second position makes sense
        delta *= -1
        if self.check_next_plus_position(delta, firstButton):
            if board[firstButton + delta] == " ":
                board[firstButton + delta] = "+"


    def check_next_plus_position(self, delta, button):
        match(delta):
            # Check left cell
            case -1:
                return button % 10 != 0
            
            # Check right cell
            case 1:
                return button % 10 != 9

            # Check top cell
            case -10:
                return button > 9
            
            # Check bottom cell
            case 10:
                return button < 90


    def run_enemy_turn(self):
        self.updatePlayerBoardFlag = True
        button = self.enemyPlayer.take_shot()
        cell = self.playerBoard[button]

        while cell == "O":
            self.playerBoard[button] = "X"
            self.enemyPlayer.update_vision(button, "X")

            if self.boardFunctions.is_ship_sunk(self.playerBoard, button):
                self.boardFunctions.place_border_marks(self.playerBoard, self.boardFunctions.shipCells, "-")
                self.enemyPlayer.update_ship_sunk()


            button = self.enemyPlayer.take_shot()
            cell = self.playerBoard[button]

        else:
            self.enemyPlayer.update_vision(button, "●")
            self.playerBoard[button] = "●"

        self.gameState = 1


    def get_status_text(self):
        # Ship placing phase
        match(self.gameState):
            case 0:
                if self.is_softlocked():
                    return "Wow, congrats on getting softlocked. Go press that reset button you dork :p"
                
                shipLength = len(self.currentShipCells)
                currentShipSize = self.shipSize
                if currentShipSize == 1:
                    return "Click on an empty space to place a 1 long ship."
                elif shipLength == 0:
                    return f"Click on an empty space to start placing a {currentShipSize} long ship."
                elif shipLength == 1:
                    return f"Click on a '*' to extend this {currentShipSize} long ship."
                else:
                    return f"Click on a '+' to extend this {currentShipSize} long ship."
        
            case 1:
                return "Play phase. Click on an enemy grid to take a shot."
            case 2:
                return "Wait does this even show up?"
            case 3:
                return "You won! Thank you for playing :3"
            case 4:
                return "You lost! Still, thank you for playing :3"
        
        return "Something happened. :O"
    

    def is_softlocked(self):
        shipLength = len(self.currentShipCells)

        # You placed the first ship segment, but there aren't any free spaces to extend that ship
        if shipLength == 1 and not "*" in self.playerBoard:
            return True
        
        # You placed more than one ship segment, but there aren't any free spaces to extend that ship
        if shipLength > 1 and not "+" in self.playerBoard:
            return True
        
        return False


    def get_score_text(self):
        if self.gameState == 0:
            return "N/A"
        
        return f"You {self.playerBoard.count('O')} : {self.enemyBoard.count('O')} Bot"