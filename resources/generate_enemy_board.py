import random
from resources.generic_board_stuff import BoardStuff

class GenerateEnemyBoard:

    def __init__(self):
        self.boardFunctions = BoardStuff()

    
    def generate_ships(self):
        self.enemyBoard = self.boardFunctions.make_empty_board(" ")
        # Place one 4 long ship
        self.place_longship(self.enemyBoard, 4)

        # Place two 3 long ships
        self.place_longship(self.enemyBoard, 3)
        self.place_longship(self.enemyBoard, 3)

        # Place three 2 long ships
        self.place_longship(self.enemyBoard, 2)
        self.place_longship(self.enemyBoard, 2)
        self.place_longship(self.enemyBoard, 2)

        # Place four 1 long ships
        self.place_smallship(self.enemyBoard)
        self.place_smallship(self.enemyBoard)
        self.place_smallship(self.enemyBoard)
        self.place_smallship(self.enemyBoard)

        # Clear border marks
        self.boardFunctions.clear_cell_markings(self.enemyBoard, "-")
        # print(self.enemyBoard)
        return self.enemyBoard


    def place_longship(self, board, length):
        searchPosition = True
        while searchPosition:
            # Randomize ship orientation
            shipDirection = bool(random.getrandbits(1))
            # False - horizontal
            # True - vertical

            # Check if the position is valid for vertical ship
            if shipDirection:
                cellOffset = 10
                startX = random.randint(0, 9)
                startY = random.randint(0, 10 - length) # 10 here cuz length effectively should be 1 shorter (4 = 0,1,2,3)
                startPos = startX + startY * 10

                #Exit while loop if this stays False 
                searchPosition = False
                for i in range(length):
                    if board[startPos + i * cellOffset] != " ":
                        searchPosition = True


            # Check if the position is valid for horizontal ship
            else:
                cellOffset = 1
                startX = random.randint(0, 10 - length) # 10 here cuz length effectively should be 1 shorter (4 = 0,1,2,3)
                startY = random.randint(0, 9)
                startPos = startX + startY * 10

                #Exit while loop if this stays False 
                searchPosition = False
                for i in range(length):
                    if board[startPos + i * cellOffset] != " ":
                        searchPosition = True
        
        # Loop exited - ship position makes sense. Now to add it
        shipCells = []
        for i in range(length):
            cellPos = startPos + i * cellOffset
            board[cellPos] = "O"
            shipCells.append(cellPos)
        
        # Place ship borders
        self.boardFunctions.place_border_marks(board, shipCells, "-")


    def place_smallship(self, board):
        searchPosition = True
        while searchPosition:
            startPos = random.randint(0, 99)
            if board[startPos] == " ":
                searchPosition = False
        
        board[startPos] = "O"

        shipCells = []
        shipCells.append(startPos)
        self.boardFunctions.place_border_marks(board, shipCells, "-")


