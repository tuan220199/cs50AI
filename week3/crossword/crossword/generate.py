import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }
    def print_demo(self):
        pass                                           

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            length = variable.length
            new = self.domains[variable].copy()
            for word in new:
                if len(word) != length:
                   self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlaps_list=[]
        for [v1,v2] in self.crossword.overlaps:
            if (x == v1 and y == v2):
                overlaps_list.append(self.crossword.overlaps[v1,v2])
        domainsx = self.domains[x].copy()
        domainsy = self.domains[y].copy()
        valuex_set = {}
        for i,j in overlaps_list:
            for value_x in domainsx:
                count = 0
                for value_y in self.domains[y]:
                    if value_x[i] != value_y[j]:
                        count +=1
                if count == len(domainsy):
                    self.domains[x].remove(value_x)
                    revised = True 
        return revised       
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []
            for variable1 in self.crossword.words:
                for variable2 in self.crossword.words:
                    arcs.append([variable1,variable2])
        else:
            for x,y in arcs:
                if revised(x,y):
                    if len(self.domains[x]) == 0:
                        return False
                    else:
                        for neighbor in self.crossword.neighbors(x):
                            if neighbor == y:
                                continue
                            else:
                                arcs.append([x,neighbor])
        return True 

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            if assignment[variable] not in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for variable1 in assignment:
            word1 = assignment[variable1]
            if len(word1) != variable1.length:
                return False
            for variable2 in assignment:
                if variable1 == variable2:
                    continue
                word2 = assignment[variable2]
                if word1 == word2:
                    return False
                overlap = self.crossword.overlaps(variable1,variable2)
                if overlap is not None:
                    i,j = overlap
                    if word1[i] == word2[j]:
                        return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        dict_value = {}

        value = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        for i in value:
            if i in assignment:
                continue
            else:
                count = 0
                for j in neighbors:
                    if i in self.domains[j]:
                        count += 1
                dict_value[i] = count
        dict_value = sorted(dict_value, key= lambda k: dict_value[k])
        
        return dict_value
        
    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variable_assignment = assignment.keys()
        unassigned_s = self.crossword.variables - variable_assignment
        unassigned_set =[]
        for item in unassigned_s:
            unassigned_set.append(item)
        
        domains_number = []
        for variable in unassigned_set:
            domains_number.append(len(self.domains[variable]))

        neighbors_number = []
        for varibale in unassigned_set:
            neighbors_number.append(len(self.crossword.neighbors(variable))) 

        unassigned_list = []
        for i in range(len(unassigned_set)):
            unassigned_list.append([unassigned_set[i],domains_number[i],neighbors_number[i]])
        unassigned_list = sorted(unassigned_list,key = lambda k:k[1])

        min_value = len(self.crossword.words) + 1
        for item in unassigned_list:
            if item[1] < min_value:
                min_value = item[1]

        for item in unassigned_list:
            if item[1] != min_value:
                unassigned_list.remove(item)

        unassigned_list = sorted(unassigned_list,key = lambda k:k[2], reverse = True)

        return unassigned_list[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            result = self.backtrack(assignment)
            if result is not None:
                return result
            assignment[variable] = None
        return None 


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
