def reachTheEnd(grid, maxTime):
    # Write your code here
    location_row = 1
    location_col = 1
    move = [[1,1]]
    if maxTime < len(grid):
        return "No"
    for i in range(maxTime):

        if location_row == len(grid) and location_row == len(grid):
            return "Yes"
        if grid[location_row][location_col] == '.':
            location_row += 1
            location_col += 1
        else:
            if grid[location_row - 1][location_col] == '.':
                location_col += 1
            elif grid[location_row ][location_col - 1] == '.':
                location_row += 1
    if location_row == len(grid) and location_row == len(grid):
        return "Yes"
    return "No"



























#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'reachTheEnd' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING_ARRAY grid
#  2. INTEGER maxTime
#

def reachTheEnd(grid, maxTime):
    # Write your code here
    location_row = 1
    location_col = 1
    moves = [[1,1]]
    new_moves = []
    if maxTime < len(grid):
        return "No"
    if len(grid) == 2:
        return "Yes"
    for i in range(maxTime):
        moves = new_moves[:]
        new_moves = []
        for move in moves:
            if move[0] == len(grid) and move[1] == len(grid):
                return "Yes"
            if grid[move[0]][move[1]] == '.':
                new_moves += [[move[0] + 1, move[0] + 1]]
            if grid[location_row - 1][location_col] == '.':
                new_moves += [[move[0], move[0] + 1]]
            if grid[location_row ][location_col - 1] == '.':
                new_moves += [[move[0] + 1, move[0]]]
    for move in new_moves:
        if move[0] == len(grid) and move[1] == len(grid):
            return "Yes"
    return "No"





if __name__ == '__main__':