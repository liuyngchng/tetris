# -*- coding:utf-8 -*-
import logging
from numpy import array
import math

"""
 This file is the core of the El-Tetris algorithm.

 Features that are used by the algorithm are implemented here.
"""

def eval_grade_ei_decimal(board: dict, position: dict) -> float:
    """
    Evaluate the board, giving a higher score to boards that "look" better.
    * landing_height: the row at which the last piece was played
    * piece: the last piece played
    * rows_removed: how many rows were removed in the last move
    :param board: a Matrix data structure

    :param position: position of the solid point of the piece

      Returns:
        A number indicating how "good" a board is, the higher the number, the
       better the board.
    """
    # trim_board(board)
    number_of_columns = get_number_of_columns(board)
    # logging.info('number_of_columns= %d', number_of_columns)
    number_of_rows = get_number_of_rows(board)
    # logging.info('number_of_rows= %d', number_of_rows)
    score = 0
    ld_height = get_landing_height(position, number_of_rows)
    # logging.info('ld_height= %d', ld_height)
    FULLROW = math.pow(2, number_of_columns) - 1;
    # logging.info('FULLROW= %d', FULLROW)
    board_decimal = get_decimal(board)
    # logging.info('board_decimal = %s', board_decimal)
    row_rm = get_rows_removed(board_decimal, FULLROW)
    # logging.info('row_rm = %s', row_rm)
    row_trans = get_row_transitions(board_decimal, number_of_columns)
    # logging.info('row_trans = %s', row_trans)
    col_trans = get_column_transitions(board_decimal, number_of_columns)
    # logging.info('col_trans = %s', col_trans)
    holes = get_hole_number(board_decimal, number_of_columns)
    # logging.info('holes = %s', holes)
    wells = get_well_sums(board_decimal, number_of_columns)
    # logging.info('wells = %s', wells)
    score += ld_height * -4.500158825082766
    score += row_rm * 3.4181268101392694
    score += row_trans * -3.2178882868487753
    score += col_trans * -9.348695305445199
    score += holes * -7.899265427351652
    score += wells * -3.3855972247263626
    return score


def get_decimal(board: list):
    """get a decimal list of a matrix of binary value in a row"""
    decimal = []
    temp = 0
    for idx, row in enumerate(board):
        for idx, col in enumerate(row):
            temp += col * math.pow(2, idx)  
        decimal.append(int(temp))
        temp = 0
    decimal.reverse()
    return decimal

def trim_board(board: list):
    line_trimmed = 0
    for index, row in enumerate(board):
        if not sum(row):
            line_trimmed += 1
            board.pop(index)  # remove empty line
    return line_trimmed


def get_landing_height(position: dict, rows: int) -> int:
    """when current piece drop down，the distance between 
    the center of the piece and the bottom of the matrix"""
    count = 0
    y_sum = 0
    for cor in position:
        y_sum += cor[0]
        count += 1
    return rows - 1 - y_sum/count


def get_number_of_rows(board: list) -> int:
    return len(board)


def get_number_of_columns(board: list) -> int:
    return len(board[0])


def get_rows_removed(board: list, full_row) -> int:
    """after shape drop down，count the line fulling of solid points"""
    solid_rows = 0
    for row in board:
        if row == full_row:
            solid_rows += 1
    return solid_rows


def get_row_transitions(board: list, num_columns: int) -> int:
    """
    The total number of row transitions.
    A row transition occurs when an empty cell is adjacent to a filled cell
    on the same row and vice versa.
    """
    transitions = 0
    last_bit = 1
    for i in range(len(board)):  # origin ++i
        row = board[i]
        #if not row:
        #    transitions += 2
        #    last_bit = 1
        #    continue
        for j in range(num_columns):  # origin ++j
            bit = (row >> j) & 1
            if bit != last_bit:
                transitions += 1
            last_bit = bit
        if bit == 0:
            transitions += 1
        last_bit = 1
    return transitions


def get_column_transitions(board: list, num_columns: int) -> int:
    """
    The total number of column transitions.
    A column transition occurs when an empty cell is adjacent to a filled cell
    on the same row and vice versa.
    """
    transitions = 0
    last_bit = 1
    for i in range(num_columns):    # ++i
        for j in range(len(board)):  # ++j
            row = board[i]
            bit = (row >> i) & 1
            if bit != last_bit:
                transitions += 1
            last_bit = bit
        last_bit = 1
    return transitions


def get_hole_number(board: list, num_columns: int) -> int:
    """
    get hole count number
    """
    holes = 0
    row_holes = 0x0000
    previous_row = board[len(board) - 1]
    
    for i in range(len(board) - 2, -1, -1):
        row_holes = ~board[i] & (previous_row | row_holes)
        for j in range(num_columns):  # ++j
            holes += ((row_holes >> j) & 1)
        previous_row = board[i]
    return holes
    


def get_well_sums(board: list, num_columns: int) -> int:
    """
     A well is a sequence of empty cells above the top piece in a column such
     that the top cell in the sequence is surrounded (left and right) by occupied
     cells or a boundary of the board.
  
     Args:
        board - The game board (an array of integers)
       num_columns - Number of columns in the board
    
     Return:
        The well sums. For a well of length n, we define the well sums as
        1 + 2 + 3 + ... + n. This gives more significance to deeper holes.
    """
    well_sums = 0

    # Check for well cells in the "inner columns" of the board.
    # "Inner columns" are the columns that aren't touching the edge of the board.
    for i in range(1, num_columns - 1):  # ++i
        for j in range(len(board) - 1, -1, -1):  # --j
            if (((board[j] >> i) & 1) == 0) \
                and (((board[j] >> (i - 1)) & 1) == 1) \
                and (((board[j] >> (i + 1)) & 1) == 1):
                # Found well cell, count it + the number of empty cells below it.
                well_sums += 1

                for k in range(j - 1, -1, -1):  # --k
                    # todo
                    if (not (board[k] >> i) & 1 ) \
                        and (board[k] >>(i - 1)) & 1 \
                        and (board[k] >>(i + 1)) & 1:
                        well_sums += 1
                    else:
                        break

    # Check for well cells in the leftmost column of the board.
    for j in range(len(board) - 1, -1, -1):  # --j
        if (not ((board[j] >> 0) & 1)) and ((board[j] >> 1) & 1):
            # Found well cell, count it + the number of empty cells below it.
            well_sums += 1
            for k in range(j - 1, -1, -1):
                if not ((board[k] >> 0) & 1):
                    well_sums += 1
                else:
                    break

    # Check for well cells in the rightmost column of the board.
    for j in range(len(board) - 1, -1, -1):  # --j
        if not ((board[j] >> (num_columns - 1)) & 1) \
            and ((board[j] >> (num_columns - 2)) & 1):
            # Found well cell, count it + the number of empty cells below it.
            well_sums += 1
            for k in range(j - 1, -1, -1):  # --k
                if not (board[k]>> (num_columns - 1) & 1):
                    well_sums += 1
                else:
                    break
    return well_sums
