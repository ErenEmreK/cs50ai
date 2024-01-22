import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines
        
def cells_around(cell):
    """
    Returns all cells around a cell as list of tuples
    """
    cells_around_cell = set()
    x, y = cell[0], cell[1]
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):            
            if not(i > 7) and not(i < 0) and not(j > 7) and not(j < 0):
                if not ((i == x) and (j == y)):
                    cells_around_cell.add(tuple((i, j)))
    return list(cells_around_cell)

def board_cells_list(height = 8, width = 8):
    board_list = []
    for column in range(height):
        for row in range(width):
            board_list.append(tuple((column, row)))
    return board_list
            
class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
                               
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        For every cell around a cell: if number of cell > mines_around_cell 
        """
        cells = self.cells
        mines = set()
        if self.count == len(cells):
            for cell in cells:
                mines.add(cell)           
        return mines
        
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        First it looks if it has a 0 around it, adds the cell to safe it is
        Then looks if cell has enough mines around them to match the number they wear
        """
        cells = self.cells
        safes = set()
        if self.count == 0:
            for cell in cells:
                safes.add(cell)
        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
                     
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            
class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        self.count_for_cell = {}

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            
    def sentence_update(self, sentence):
        #todo if sentence is useless delete from knowledge after adding all to mines or safes
        #todo rearranging all the sentences with self.mines and safes infos
                
        for cell in sentence.cells.copy():
            if (cell in self.safes):
                sentence.cells.remove(cell) 
            if (cell in self.mines):
                sentence.cells.remove(cell)
                sentence.count -= 1
        
        if sentence.count == 0:#4
            for cell in sentence.cells:
                self.safes.add(cell)
            self.knowledge.remove(sentence)
        elif len(sentence.cells) == sentence.count:
            for cell in sentence.cells:
                self.mines.add(cell)
            self.knowledge.remove(sentence)
        else:      
            for a_sentence in (self.knowledge):#5subset method
                if (a_sentence != sentence) and sentence in self.knowledge:
                    if a_sentence.cells.issubset(sentence.cells):
                        inferrence = Sentence((sentence.cells - a_sentence.cells), (sentence.count - a_sentence.count))
                        self.knowledge.append(inferrence)
                        self.knowledge.remove(sentence)
                    
                    elif sentence.cells.issubset(a_sentence.cells):
                        inferrence = Sentence((a_sentence.cells - sentence.cells), (a_sentence.count - sentence.count))
                        self.knowledge.append(inferrence)
                        self.knowledge.remove(a_sentence)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)#1 mark move made
        self.mark_safe(cell)#2 marks the cell itself safe
        
        cells_around_to_add = cells_around(cell)#3 create new sentence for nearby mines
        new_sentence = Sentence(cells_around_to_add, count)
        self.knowledge.append(new_sentence)
        self.sentence_update(new_sentence)
        
        for sentence in self.knowledge:#6 try to make new inferrences
            self.sentence_update(sentence)
                   
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_move in self.safes:
            if safe_move not in self.moves_made:
                return safe_move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cells_list = board_cells_list()
        random.shuffle(cells_list)
        for random_move in cells_list:
            if random_move not in self.moves_made and random_move not in self.mines:
                return random_move
        return None
        