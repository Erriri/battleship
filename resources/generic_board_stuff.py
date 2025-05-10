
class BoardStuff():

    def make_empty_board(self, char):
        # Board = [[char for i in range(10)] for j in range(10)]
        Board = [char for i in range(100)]
        return Board


    def clear_cell_markings(self, board, char):
        for i in range(100):
            if board[i] == char:
                board[i] = " "
    
    
    def place_border_marks(self, board, cells, char):
        # For ships up to 4 long, we only need to do this for first and last cell
        endCells = []
        endCells.append(cells[0])
        endCells.append(cells[-1])
        
        for cell in endCells:
            # left
            if cell % 10 > 0 and board[cell - 1] == " ":
                board[cell - 1] = char

            # right
            if cell % 10 < 9 and board[cell + 1] == " ":
                board[cell + 1] = char

            # top
            if cell > 9 and board[cell - 10] == " ":
                board[cell - 10] = char

            # bottom
            if cell < 90 and board[cell + 10] == " ":
                board[cell + 10] = char
            
            # top left
            if cell % 10 > 0 and cell > 9 and board[cell - 11] == " ":
                board[cell - 11] = char
            
            # top right
            if cell % 10 < 9 and cell > 9 and board[cell - 9] == " ":
                board[cell - 9] = char
            
            # bottom left
            if cell % 10 > 0 and cell < 90 and board[cell + 9] == " ":
                board[cell + 9] = char
            
            # bottom right
            if cell % 10 < 9 and cell < 90 and board[cell + 11] == " ":
                board[cell + 11] = char
    

    def is_ship_sunk(self, board, cell):
        # List of cells that are part of the (sunk) ship. Used for generating the border
        self.shipCells = [cell]

        # if cell is "O" - return false, ship is still floating
        # if cell is "X" - check the next cell in the line

        # Start checking with left, then right, then top, then bottom.
        for direction in range(4):
            startingCell = cell

            # How far are we checking. Ships longer than 4 don't exist here, so 3 checks should be fine
            for i in range(3):

                # See if that cell exists
                currentCell = self.check_cell(startingCell, direction)

                if currentCell:
                    # If it is "O", we are done here
                    if board[currentCell] == "O":
                        return False
                    # If it is "X", proceed
                    elif board[currentCell] == "X":
                        # Save it for the future
                        self.shipCells.append(currentCell)

                        # If the array is 4 long, we are done here
                        if len(self.shipCells) > 3:
                            return True
                        
                        # Otherwise, continue search. Shift the cell
                        startingCell = currentCell


                    # Cell isn't part of a ship, no need to check beyond
                    else:
                        break
                        
                # Cell doesn't exist, no need to check beyond
                else:
                    break

        # All directions checked, no unsunk ship cells
        return True
        

    # See if a cell in a specified direction exists, return that cell if it does
    def check_cell(self, cell, direction):
        match(direction):
            case 0: # "left"
                if cell % 10 > 0:
                    return cell - 1

            case 1: # "right"
                if cell % 10 < 9:
                    return cell + 1

            case 2: # "top"
                if cell > 9:
                    return cell - 10

            case 3: # "bottom"
                if cell < 90:
                    return cell + 10

        # No such cell       
        return False


    def is_game_over(self, board):
        return not "O" in board
