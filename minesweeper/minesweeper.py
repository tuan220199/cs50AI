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
        """
        if self.count == len(self.cells):
            return self.cells
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -=1 
        return None 
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return None 
        raise NotImplementedError


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
        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # mark the cell as safe
        self.mark_safe(cell)

        #add a new sentence to the AI's knowledge base, based on the value of `cell` and `count`
        # create all the neighbor of each cell
        neighbors = set()
        for i in range(cell[0]-1,cell[0]+2):
            for j in range(cell[1]-1,cell[1]+2):
                if i >= 0 and i < self.height and j >= 0 and j < self.width:
                    neighbor_cell = (i,j)
                    neighbors.add(neighbor_cell)

        # remove cell itself out of the neigbor
        if cell in neighbors:
            neighbors.remove(cell)

        # check to remove mine cell or safe cell known before
        neighbors_copy = neighbors.copy()
        for neighbor in neighbors_copy:
            if neighbor in self.mines:
                neighbors.remove(neighbor)
                count -= 1
            if neighbor in self.safes:
                neighbors.remove(neighbor)

        # create sentence of each cell when we have cell neighbor and count, then add it to the knowledge  
        sentence = Sentence(neighbors,count)
        self.knowledge.append(sentence)

        # check the cell in sentence's neigbor is mine or safe or not, if yes 
        #then update other sentences in knowledge
        for sentence in self.knowledge:
            if sentence.count == 0:
                sentence.cells_copy = sentence.cells.copy()
                for cell in sentence.cells_copy:
                    self.mark_safe(cell)

        for sentence in self.knowledge:
            if sentence.count == len(sentence.cells):
                sentence.cells_copy = sentence.cells.copy()
                for cell in sentence.cells_copy:
                    self.mark_mine(cell)

        # check sentence A is subset of sentence B or not
        for sentenceA in self.knowledge:
            for sentenceB in self.knowledge:
                if sentenceA == sentenceB:
                    continue
                elif len(sentenceA.cells) == 0:
                    continue
                elif len(sentenceB.cells) == 0:
                    continue
                elif sentenceA.cells.issubset(sentenceB.cells):
                    sentence = Sentence(sentenceB.cells - sentenceA.cells,sentenceB.count - sentenceA.count)
                    if sentence not in self.knowledge:
                        self.knowledge.append(sentence)
                elif sentenceB.cells.issubset(sentenceA.cells):
                    sentence = Sentence(sentenceA.cells - sentenceB.cells, sentenceA.count - sentenceB.count)
                    if sentence not in self.knowledge:
                        self.knowledge.append(sentence)
        return None

        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made:
                    if (i,j) in self.safes:
                        return (i,j)

        return None        
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made:
                    if (i,j) not in self.mines:
                        return (i,j)
        return None
        raise NotImplementedError
