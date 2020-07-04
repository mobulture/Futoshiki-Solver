# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 20:34:22 2020

@author: ezhu2
"""

import copy

def fill(board,row,col,value):
    new_board = copy.deepcopy(board)
    new_board[int(row)][int(col)] = value
    return new_board

class Futoshiki_Solver:
    def __init__(self,board,hor_res,ver_res):
        self.board = board # Our game board
        self.hor_dict = hor_res # Our horizontal restrictions
        self.ver_dict = ver_res  #Our vertical restrictions
        self.board_array = []
        self.filled = {} # Dict of values that have been filled
        self.domains= {} # Keep track of domains of variables
        self.find_filled()
        for item in self.filled: # Minimize domain of rows and columns that already have a number value
            self.forward_check(item)
            
    def check_filled(self):
        return not self.domains #Check if board is completely filled or not
    
    def find_filled(self):
        self.print_board()
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if(self.board[i][j] != '0'):
                    print(str(i) + ','+ str(j))
                    self.board_array.append((i,j,self.board[i][j]))
                    self.filled[str(i) +","+ str(j)] = self.board[i][j] #Constrain domain for already selected variables
                else:
                    self.domains[str(i) + "," + str(j)] = ['1','2','3','4','5'] #Initialize domain for unknown variables
                                        
    def print_domain(self):
        for item in self.domains:
            print("Key : {} , Value : {}".format(item,self.domains[item]))
                
    def print_board(self):
        print_val = ""
        for i in self.board:
            line = ""
            for j in i:
                line += (j + " ")
            print(line)
            line += ("\n")
            print_val += line
        print("")
        return print_val
   
    def restrict_right(self,index, right_ind): #Restrict domain on cell to the right if it has a < or > symbol
        if (self.hor_dict[index] == '<'):
                old_domain = self.domains[right_ind]
                self.domains[right_ind] = [old_val for old_val in old_domain if old_val > self.filled[index]] #Keep only values less than values to the right
        if (self.hor_dict[index] == '>'): 
                old_domain = self.domains[right_ind]
                self.domains[right_ind] = [old_val for old_val in old_domain if old_val < self.filled[index]] 
 
    def restrict_left(self,index, left_ind):# Restrict domain on cell to the left if it has a < or > symbol

        if (self.hor_dict[left_ind] == '<'):
                old_domain = self.domains[left_ind]
                self.domains[left_ind] = [old_val for old_val in old_domain if old_val < self.filled[index]] #Keep only values less than values to the right
        if (self.hor_dict[left_ind] == '>'): 
                old_domain = self.domains[left_ind]
                self.domains[left_ind] = [old_val for old_val in old_domain if old_val > self.filled[index]] 

    def restrict_bottom(self,index,bot_ind): #Same but for bottom
        if (self.ver_dict[index] == 'v'):
                old_domain = self.domains[bot_ind]
                self.domains[bot_ind] = [old_val for old_val in old_domain if old_val < self.filled[index]] #Keep only values less than values to the bottom
        if (self.ver_dict[index] == '^'):
                old_domain = self.domains[bot_ind]
                self.domains[bot_ind] = [old_val for old_val in old_domain if old_val > self.filled[index]] 

    def restrict_top(self,index,top_ind): # Same but for top
        if (self.ver_dict[top_ind] == 'v'):
                old_domain = self.domains[top_ind]
                self.domains[top_ind] = [old_val for old_val in old_domain if old_val > self.filled[index]] #Keep only values less than values to the bottom
        if (self.ver_dict[top_ind] == '^'): 
                old_domain = self.domains[top_ind]
                self.domains[top_ind] = [old_val for old_val in old_domain if old_val < self.filled[index]] 


    def forward_check(self,item):
        value = self.filled[item]
       # count = 0; #Keep count of how many variables restricted, each space counts as 1, greater than or less thans also count as another restriction
        indices = item.split(',')
        row = int(indices[0])
        col = int(indices[1])
        for i in range (5): #Iterate horizontally
            if i != col:
                cur_index = str(row) + ',' + str(i) 
                if(cur_index in self.domains): #If the slot is already filled, result would be a string
                        if (value in self.domains[cur_index]):
                            self.domains[cur_index].remove(value)
                            if  not self.domains[cur_index]:
                                return False
        
        for j in range(5):#Iterate vertically
            if j != row:  
                cur_index = str(j) + ',' + str(col)            
                if(cur_index in self.domains): # Start decreaseing domain of space on index
                        if (value in self.domains[cur_index]):
                            self.domains[cur_index].remove(value)

        if( col <= 3): #Starting to check horizontal constraints. check all but rightmost col
            if(item in self.hor_dict):               
                right_ind = str(row)+',' + str(col+1) #Index of the number adjacent to the right
                if(right_ind in self.domains): #Decrease domain of numbers around
                    self.restrict_right(item,right_ind)
        if(col > 0): # Check all but leftmost col
            left_ind= str(row)+',' + str(col-1)
            if(left_ind in self.hor_dict and left_ind in self.domains):        
                    self.restrict_left(item,left_ind)
#                    if not self.domains[left_ind]:
#                        return false
        if(row <= 3): #Start for vertical constraints, all but last row
            if item in self.ver_dict:
                bottom_ind = str(row+1)+',' + str(col) #Index of the number adjacent to the bottom
                if (bottom_ind in self.domains):
                    self.restrict_bottom(item,bottom_ind)
#                if not self.domains[bottom_ind]:
#                    return false
        if(row > 0): #All but first row
            top_ind = str(row-1)+',' + str(col)
            if top_ind in self.ver_dict and  top_ind in self.domains:
                self.restrict_top(item,top_ind)
#                if not self.domains[top_ind]:
#                    return false        
                       
    def count_constraints(self,item): #Iterates similarly to forward checking, however this program simply counts the amount of constraints, does not remove constraints
        count = 0; #Keep count of how many variables restricted, each space counts as 1, greater than or less thans also count as another restriction
        indices = item.split(',')
        row = int(indices[0])
        col = int(indices[1])
        for i in range (5): #Iterate horizontally
            if i != col:
                index = str(row) + ',' + str(i) 
                if(index in self.domains): #If the slot is already filled, result would be a string
                    count += 1

        for j in range(5):#Iterate vertically
            if j != row:  
                index = str(j) + ',' + str(col)            
                if(index in self.domains): # Start decreaseing domain of space on index                   
                    count += 1
        if( col <= 3): #Starting to check horizontal constraints. check all but rightmost col
            if(item in self.hor_dict):               
                count+=1
        if(col > 0): # Check all but leftmost col
            left_ind= str(row)+',' + str(col-1)
            if(left_ind in self.hor_dict):
                count+=1             
        if(row <= 3): 
            if item in self.ver_dict:
              count+=1
        if(row > 0): #All but first row
            top_ind = str(row-1)+',' + str(col)
            if top_ind in self.ver_dict:
                count+=1
                               
        return count

    def pick_variable(self): #Picks next step to explore based off of heuristics
        max_constraint = 999
        for i in self.domains.values():
            if len(i) < max_constraint:
                max_constraint = len(i)
        #Create list of all variables with the most constraints currently
        to_choose = [max_constrained_variables for max_constrained_variables in self.domains.keys() if len(self.domains[max_constrained_variables]) == max_constraint]
        if max_constraint  == 0: # If a variable has no remaining domain
            print("um hello")
            return False
        if len(to_choose) == 1: #If one variable has more constraints than the rest pick it
            return to_choose[0]
        else: #Otherwise, tie break using most constraining variable
            most_constraining = 0
            for index in to_choose: #For each possible next_choice, choose the one that constrains the most
                    most_constraining = self.count_constraints(index) # Update the max constrainer
            #Select indices now with equal most_constraining variables
            to_choose = [max_constraining_variable for max_constraining_variable in to_choose if self.count_constraints(max_constraining_variable) == most_constraining]
        #Since can pick arbitrarily now, we'll just go with the first value
            return to_choose[0]
        
    
    def fill_puzzle(self,moves): #Fill in the puzzleboard with a sequence of mof3w
        for step in moves:
            row = int(step[0])
            col = int(step[1])
            self.board[row][col] = step[2]
            del self.domains[str(row) + ',' + str(col)] #We need to delete the domain now that the spot is filled
        
            
            
def back_track(puzzle,current_solution = []): #Prints a list of moves to make if there is one, else returns False
    if puzzle.check_filled(): #Base case, check if the puzzle is completely filled in
        return current_solution # Return the list of steps we have made to get this far
    to_fill = puzzle.pick_variable() #Index of variable to fill
    if to_fill == False:
        print("false")
        return False

    for value in puzzle.domains[to_fill]:
        #Find indices of board to fill
        row = to_fill.split(',')[0]
        col = to_fill.split(',')[1]
        new_board = fill(puzzle.board,row,col,value) #Create a new board after filling in variable with value
        new_puzzle = Futoshiki_Solver(new_board,puzzle.hor_dict,puzzle.ver_dict) # Create new futoshiki state, constructor also forward checks
        
        current_solution.append((row,col,value)) # This is to keep track of the moves we have made
        result = back_track(new_puzzle,current_solution) # Start recursing
        if result != False: #Only returns False if there is no solution, otherwise, continue
            return result
        current_solution.remove((row,col,value))

    return False
        

        
        
        
if __name__ == "__main__":
    read_file = input("Enter filename: ")
    f = open(read_file,'r')
    line_count = 0
    board = []
    while(line_count <= 4): # Read input board state
        curr_line  = f.readline()
        tiles  = curr_line.split() 
        board.append(tiles)
        line_count += 1
    
    f.readline()
    hor_res = []
    line_count = 0
    while(line_count <= 4): # Read horizontal restrictions
        curr_line = f.readline()
        tiles = curr_line.split()
        hor_res.append(tiles)
        line_count += 1
        
    f.readline()
    ver_res = []
    line_count = 0
    while(line_count <= 3): # Read horizontal restrictions
        curr_line = f.readline()
        tiles = curr_line.split()
        ver_res.append(tiles)
        line_count += 1
    ver_dict = {} #Gather all of the veritcal restrictions using key value pair
    for i in range (len(ver_res)):
            for j in range(len(ver_res[i])):
                if(ver_res[i][j] != '0'):
                    ver_dict[str(i) + "," + str(j)] = ver_res[i][j] 
    hor_dict={} #Gather all of the horizontal restrictions in key value pair
    for i in range (len(hor_res)):
        for j in range(len(hor_res[i])):
            if(hor_res[i][j]!= '0'):
                hor_dict[str(i) + "," + str(j)] = hor_res[i][j]
                
    solver = Futoshiki_Solver(board,hor_dict,ver_dict)
    solver.print_domain()
    results = back_track(solver)
    if results != False:
        solver.fill_puzzle(results)
        solver.print_board()
        solver.print_domain()
    output_file_name = input("Enter output file name\n")
    output_file = open(output_file_name,"w")
    output_file.write(solver.print_board())