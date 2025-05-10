import random
from resources.generic_board_stuff import BoardStuff

# The plan:
# If enemy hit a ship, try to sink it
# Otherwise, use one of the two prepared templates to hunt for a big ship
# 24-26 shots, depending on the template
# After that switch to random shots

class EnemyPlayer():
    
    def __init__(self):
        self.boardFunctions = BoardStuff()
        self.playerBoardSight = self.boardFunctions.make_empty_board(" ")

        self.focusedShip = []

        self.chosenShotTemplate = self.generate_shot_template()
    

    def update_vision(self, cell, char):
        self.playerBoardSight[cell] = char
        if char == "X":
            self.focusedShip.append(cell)


    def update_ship_sunk(self):
        self.boardFunctions.place_border_marks(self.playerBoardSight, self.focusedShip, "-")
        self.focusedShip = []


    def take_shot(self):
        # Step 1 - try to hit neighbors of a hit ship
        if len(self.focusedShip) > 0:
            potentialShots = []

            # You hit the ship once, it can be in any direction
            if len(self.focusedShip) == 1:
                for cell in self.focusedShip:
                    for direction in range(4):
                        checkedCell = self.boardFunctions.check_cell(cell, direction)
                        if checkedCell and self.playerBoardSight[checkedCell] == " ":
                            potentialShots.append(checkedCell)
                return random.choice(potentialShots)
            
            # You hit the ship more than once, ships are straight, you should know where to fire
            self.focusedShip.sort()
            delta = self.focusedShip[1] - self.focusedShip[0]

            checkedCell = self.focusedShip[0] - delta
            if self.playerBoardSight[checkedCell] == " ":
                potentialShots.append(checkedCell)
            
            checkedCell = self.focusedShip[-1] + delta
            if self.playerBoardSight[checkedCell] == " ":
                potentialShots.append(checkedCell)
            
            return random.choice(potentialShots)


        # Step 2 - use the shot template
        if self.chosenShotTemplate:
            cell = random.choice(self.chosenShotTemplate)
            self.chosenShotTemplate.remove(cell)

            while self.chosenShotTemplate and self.playerBoardSight[cell] != " ":
                cell = random.choice(self.chosenShotTemplate)
                self.chosenShotTemplate.remove(cell)
            
            if cell:
                return cell

        # Step 3 - just pick a random cell
        cell = random.randint(0, 99)
        while self.playerBoardSight[cell] != " ":
            cell = random.randint(0, 99)
        return cell
    

    def generate_shot_template(self):
        offset = random.randint(0, 3)
        shotTemplate = []

        # Diagonals from top left to bottom right
        if bool(random.getrandbits(1)):
            start = offset
            while start < 10:
                cell = start
                while True:
                    shotTemplate.append(cell)
                    cell += 11
                    if cell % 10 == 0 or cell > 99:
                        break

                start += 4
            
            start = (4 - offset) * 10
            while start < 100:
                cell = start
                while True:
                    shotTemplate.append(cell)
                    cell += 11
                    if cell % 10 == 0 or cell > 99:
                        break

                start += 40
        
        # Diagonals from top right to bottom left
        else:
            start = 9 - offset
            while start > 0:
                cell = start
                while True:
                    shotTemplate.append(cell)
                    cell += 9
                    if cell % 10 == 9 or cell > 99:
                        break

                start -= 4
            
            start = (4 - offset) * 10 + 9
            while start < 100:
                cell = start
                while True:
                    shotTemplate.append(cell)
                    cell += 9
                    if cell % 10 == 9 or cell > 99:
                        break

                start += 40
        
        return shotTemplate



# The template:
# _ X _ _ _ X _ _ _ X
# X _ _ _ X _ _ _ X _
# _ _ _ X _ _ _ X _ _
# _ _ X _ _ _ X _ _ _
# _ X _ _ _ X _ _ _ X
# X _ _ _ X _ _ _ X _
# _ _ _ X _ _ _ X _ _
# _ _ X _ _ _ X _ _ _
# _ X _ _ _ X _ _ _ X
# X _ _ _ X _ _ _ X _

# shotTemplate1 = [9, 18, 27, 36, 45, 54, 63, 72, 81, 90, 5, 14, 23, 32, 41, 50, 1, 10, 49, 58, 67, 76, 85, 94, 89, 98]

# shotTemplate2 = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99, 4, 15, 26, 37, 48, 59, 8, 19, 40, 51, 62, 73, 84, 95, 80, 91]

# This is guaranteed to eventually hit the big ship, which should reveal a bunch of area

# The function should generate mirror and offset variations of this
