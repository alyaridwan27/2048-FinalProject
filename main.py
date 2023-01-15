#importing modules
import tkinter as tk #standard interface in python for creating graphical user interface
import random #used to generate random words from list

#creating classes
class Game(tk.Frame): #this class will inherit from the tkinter frame widget in which the game will run using this function
    def __init__(self):
        tk.Frame.__init__(self) #the frame constructor to construct a game as a frame widget
        self.grid() #this will allow us to create the game grid
        self.master.title("2048") #title that will show on the game window

        self.gridMain = tk.Frame(
            self, bg=Game.gridColor, bd=3, width=600, height=600
        ) 
        self.gridMain.grid(pady=(110,0)) #will give padding at the top for the score header
 
        self.GUImaker() #calling GUI_maker function in the constructor
        self.startGame() #calling start_game function in the constructor

        #calling all the movement functions
        self.master.bind("<Left>", self.left)
        self.master.bind("<Right>", self.right)
        self.master.bind("<Up>", self.up)
        self.master.bind("<Down>", self.down)
 
        self.mainloop() #calling main loop

    #making color coding
    gridColor = "#b8afa9"
    emptyCellColor = "#ffd5b5"
    scoreLabelFont = ("Verdana", 24)
    scoreFont = ("Helvetica", 48, "bold")
    gameOverFont = ("Helvetica", 48, "bold")
    gameOverFontColor = "#ffffff"
    bgWin = "#ffcc00"
    bgLose = "#a39489"
 
    cellsColors = {
        2: "#fcefe6",
        4: "#f2e8cb",
        8: "#f5b682",
        16: "#f29446",
        32: "#ff775c",
        64: "#e64c2e",
        128: "#ede291",
        256: "#fce130",
        512: "#ffdb4a",
        1024: "#f0b922",
        2048: "#fad74d"    
        }
 
    cellNumColor = {
        2: "#695c57",
        4: "#695c57",
        8: "#ffffff",
        16: "#ffffff",
        32: "#ffffff",
        64: "#ffffff",
        128: "#ffffff",
        256: "#ffffff",
        512: "#ffffff",
        12048: "#ffffff"
        }
 
    cellNumFonts = {
        2: ("Helvetica", 55, "bold"),
        4: ("Helvetica", 55, "bold"),
        8: ("Helvetica", 55, "bold"),
        16: ("Helvetica", 50, "bold"),
        32: ("Helvetica", 50, "bold"),
        64: ("Helvetica", 50, "bold"),
        128: ("Helvetica", 45, "bold"),
        256: ("Helvetica", 45, "bold"),
        512: ("Helvetica", 45, "bold"),
        1024: ("Helvetica", 40, "bold"),
        2048: ("Helvetica", 40, "bold"),
        }
    
    # creating a funcvtion to make GUI
    def GUImaker(self): #function to make GUI
        #make grid
        self.cells = [] #a 2D list holding the information contained in each cell of the grid 
        #make a nested loop to append cells row by row
        for i in range(4):
            row = []
            for j in range(4):
                #each cell will create a slef frame which will inherit from the main grid
                cellsFrame = tk.Frame(
                    self.gridMain,
                    bg=Game.emptyCellColor,
                    width=150,
                    height=150
                )
                #calling grid on each cell frame with i row and j collumn and adding five pixels of padding
                cellsFrame.grid(row=i, column=j, padx=5, pady=5)
                #we will pass the main grid to this and set the bg to empty cell color
                cellNum = tk.Label(self.gridMain, bg=Game.emptyCellColor)
                #create a dictionary to store data
                cell_data = {"frame":cellsFrame, "number": cellNum}
 
                cellNum.grid(row=i, column=j) #to call each of the cell display
                row.append(cell_data) #appending the dictionary
            self.cells.append(row)

            #creating score header
            scoreFrame = tk.Frame(self) #another frame variable
            scoreFrame.place(relx=0.5, y=60, anchor="center") #positioning the frame score
            #adding label that says score
            tk.Label(
                scoreFrame,
                text="Score",
                font=Game.scoreLabelFont
            ).grid(row=0)
            #displaying the actual score, setting initial score to zero, and setting the font
            self.scoreLabel = tk.Label(scoreFrame, text="0", font= Game.scoreFont)
            #placing this right below the score label
            self.scoreLabel.grid(row=1)
    
    #creating a function to start the game
    #this function will create a 4x4 matrix that will hold all the values shown on the board
    #at each turn we first initialize the matirc with all zeros
    def startGame(self):
        #create matrix of zeros
        self.matrix = [[0] * 4 for _ in range(4)]
 
        #fill 2 random cells with 2s
        row = random.randint(0,3) #returns and integer number of rows and columns from 0 to 3
        col = random.randint(0,3) #returns and integer number of rows and columns from 0 to 3
        #setting the bg color using the stored information on the GUI
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=Game.cellsColors[2])
        self.cells[row][col]["number"].configure(
            bg=Game.cellsColors[2],
            fg=Game.cellNumColor[2],
            font=Game.cellNumFonts[2],
            text="2"
        )
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]["frame"].configure(bg=Game.cellsColors[2])
        self.cells[row][col]["number"].configure(
            bg=Game.cellsColors[2],
            fg=Game.cellNumColor[2],
            font=Game.cellNumFonts[2],
            text="2"
        )
 
        self.score = 0 #keep track of the score, initialize to zero for the start
    
    #make matrix manipulation functions
    def stack(self):
        #this function compresses all nonzero numbers in the matrix to one side of the board
        #eliminating any empty spaces between them
        #matrix_1 containing all zeros is used in a nested loop for each row in the matrix
        #the function keeps track of the number of cells containing nonzero number and a variable called position fill
        #if the value in the cell is nonzero, the value in the new matric at the i-fill postion is set to the value
        #the fill position is then incremented by one, after the for loop, the original matrix is set to the new matrix
        matrix1 = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fillPosition = 0
            for j in range(4):
                if self.matrix[i][j] != 0:
                    matrix1[i][fillPosition] = self.matrix[i][j]
                    fillPosition += 1
        self.matrix = matrix1
    def combine(self):
        #this function adds together all horizontally adjacent nonzero numbers of the same value in the matrix of 2048 and merges them to the left position
        #when two tiles of the same value merge and collapse into one tile of their sum
        #in the nested loop, we are only looping until column two so we can index j+1
        #afer that we will be checking if the value at i, j in the matrix is not zero and is equal to the value i, j+1
        #the value at i, j is multiplied by 2 and the value i, j+1 is set to zero
        # the combine function updates the score by adding newly combined values to self.score
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j + 1]:
                    self.matrix[i][j] *= 2
                    self.matrix[i][j + 1] = 0
                    self.score += self.matrix[i][j]
 
    def reverse(self):
        #this function reverses the order of each row in the matrix
        #matrix_1 is an empty list 
        #the value gets reversed after the nested for loop and the original matrix is set to matrix_1
        matrix1 = []
        for i in range(4):
            matrix1.append([])
            for j in range(4):
                matrix1[i].append(self.matrix[i][3-j])
        self.matrix = matrix1
 
    def transpose(self):
        #this function flips matrix over its diagonal
        #matrix_1 of all zeros is created
        #in the nested for loop, the value at i, j in matrix_1 is set to the value at j, i in the current matrix
        #the original matrix is set to matrix_1
        matrix1 = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                matrix1[i][j] = self.matrix[j][i]
        self.matrix = matrix1
    
    #creating a function to randomly add new 2 or 4 tile to an empty cell
    def addTile(self):
        #the logic used is the same as the one applied in start_game()
        #the function rnadomly selects either 2 or 4 as the value to fill the selected empty cell
        row = random.randint(0,3)
        col = random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        self.matrix[row][col] = random.choice([2,4])

    #creating a function to update GUI to match the matrix
    def updateGUI(self):
        #updates the GUI to reflect the changes made to the matrix
        #this function uses a nested loop to iterate through the cells in the matrix and updates the appearance of the cells based on their values
        #empty cells are displayed with an empty cell color and no text
        #non-empty cells are displayed with the bg color, font color, and font type specifies in the cell's properties
        #the function updates and displays the score by calling configure() function on the score label with the current score value
        for i in range(4):
            for j in range(4):
                cellValue = self.matrix[i][j]
                if cellValue == 0:
                    self.cells[i][j]["frame"].configure(bg=Game.emptyCellColor)
                    self.cells[i][j]["number"].configure(bg=Game.emptyCellColor, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=Game.cellsColors[cellValue])
                    self.cells[i][j]["number"].configure(
                        bg=Game.cellsColors[cellValue],
                        fg=Game.cellNumColor[cellValue],
                        font=Game.cellNumFonts[cellValue],
                        text=str(cellValue)
                    )
        self.scoreLabel.configure(text=self.score)
        self.update_idletasks() #used to immediately display the updated widgets

    #create a function for pressing arrow buttons for playing the game
    def left(self, event):
        #performs a move to the left on the matrix
        self.stack() #to compress nonzero numbers to the left side of the matrix
        self.combine() #to combine horizontally adjacent numbers
        self.stack() #to eliminate newly created zero cells from the prev step
        self.addTile() #adds a new tile to the matrix
        self.updateGUI() #updates the GUI
        self.gameOver() #to check if the game is over
 
    def right(self, event):
        #performs a move to the right on the matrix
        self.reverse() #transforms the matric so that a right swipe is equivalent to a left swipe
        self.stack() #compress nonzero numbers to the left side of the matrix
        self.combine() #combine horizontally adjacent numbers
        self.stack() #to eliminate new created zero cells from prev step
        self.reverse() #to restore the matrix to its original orientation
        self.addTile() #adds a new tile to the matrix
        self.updateGUI() #updates the GUI
        self.gameOver() #to check if the game is over
 
    def up(self, event):
        #performs a move upwards on the matrix
        self.transpose() #transposes the matrix to make it work like a left move
        self.stack() #compress nonzero numbers to the left side of the matrix
        self.combine() #combine horizontally adjacent numbers
        self.stack() #to eliminate new created zero cells from prev step
        self.transpose() #transposes the matrix again to restore it to its original orientation
        self.addTile() #adds a new tile to the matrix
        self.updateGUI() #updates GUI
        self.gameOver() #to check if the game is over
 
    def down(self, event):
        self.transpose() #transposes and reverses the matrix so that a leftward move has a downward effect
        self.reverse()
        self.stack() #compress nonzero numbers to the left side of the matrix
        self.combine() #combine horizontally adjacent numbers    
        self.stack() #to eliminate new created zero cells from prev step
        self.reverse() #transposes and reverses the matrix again to restore it to its original orientation
        self.transpose()
        self.addTile() #adds a new tile to the matrix
        self.updateGUI() #updates GUI
        self.gameOver() #to check if the game is over

    #function to check if any moves are possible
    def horizontalMoves(self):
        #checks if there are any possible horizontal moves in the matric
        #it uses nested loop to check if any pair of horizonatlly adjacent cells have the same value
        #if such pair is found, the function returns "True" otherwise it returns "False"
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j + 1]:
                    return True
        return False
 
    def verticalMoves(self):
        #checks if there are any possible verical moves in the matrix
        #it uses nested loop to check if any pair of vertically adjacents cells have the same value
        #if such pair is found, the function returns "True" otherwise it returns "False"
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    #function to check if the game is over
    #uses the built-in function any() to check if there is 2048 value in any cell
    #display "YOU WIN" if there is and "GAME OVER" if there's none
    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            gameOverFrame = tk.Frame(self.gridMain, borderwidth=2)
            gameOverFrame.place(relx=0.5, rely= 0.5, anchor="center")
            tk.Label(
                gameOverFrame,
                text = "YOU WIN",
                bg=Game.bgWin,
                fg=Game.gameOverFontColor,
                font=Game.gameOverFont
            ).pack() #displays the game over frame
        elif not any(0 in row for row in self. matrix) and not self.horizontalMoves() and not self.verticalMoves():
            gameOverFrame = tk.Frame(self.gridMain, borderwidth=2)
            gameOverFrame.place(relx=0.5, rely= 0.5, anchor="center")
            tk.Label(
                gameOverFrame,
                text = "GAME OVER",
                bg=Game.bgLose,
                fg=Game.gameOverFontColor,
                font=Game.gameOverFont
            ).pack()
       
def main():
    Game()
 
if __name__ == "__main__":
    main()
