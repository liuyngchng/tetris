# -*- coding:utf-8 -*-
from numpy import array


"""
 This file is the core of the El-Tetris algorithm.

 Features that are used by the algorithm are implemented here.
"""


def eval_grade_ei(board: dict, position: dict) -> float:
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
    number_of_rows = get_number_of_rows(board)
    score = 0
    ld_height = get_landing_height(position, number_of_rows)
    row_rm = get_rows_removed(board)
    row_trans = get_row_transitions(board, number_of_columns)
    col_trans = get_column_transitions(board, number_of_columns)
    holes = get_hole_number(board, number_of_columns)
    wells = get_well_sums(board, number_of_columns)
    score += ld_height * -4.500158825082766
    score += row_rm * 3.4181268101392694
    score += row_trans * -3.2178882868487753
    score += col_trans * -9.348695305445199
    score += holes * -7.899265427351652
    score += wells * -3.3855972247263626
    return score


def trim_board(board: dict):
    line_trimmed = 0
    for index, row in enumerate(board):
        if not sum(row):
            line_trimmed += 1
            board.pop(index)  # remove empty line
    return line_trimmed


def get_landing_height(position: dict, rows: int) -> int:
    """当前方块落下去之后，方块中点距离底部的高度"""
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


def get_rows_removed(board: list) -> int:
    """after shape drop down，count the line fulling of solid points"""
    solid_rows = 0
    for index, row in enumerate(board):
        if row.count(0) == 0:
            solid_rows += 1
            board.pop(index)  # remove line full of solid points
            board.insert(0, [0] * len(board[0]))  # insert a new line instead
    return solid_rows


def get_row_transitions(board: list, num_columns: int) -> int:
    """
    The total number of row transitions.
    A row transition occurs when an empty cell is adjacent to a filled cell
    on the same row and vice versa.
    """
    transitions = 0
    last_bit = 1
    for i in range(len(board)):
        row = board[i]
        if not sum(row):
            transitions += 2
            last_bit = 1
            continue
        for j in range(num_columns):
            bit = row[j]
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
    board_t = array(board).T
    transitions = 0
    last_bit = 1
    for i in range(num_columns):
        column = board_t[i]
        if not sum(column):
            transitions += 1
            last_bit = 1
            continue
        for j in range(len(board)):
            bit = column[j]
            if bit != last_bit:
                transitions += 1
            last_bit = bit
        last_bit = 1
    return transitions


def get_hole_number(board: list, num_columns: int) -> int:
    """
    get hole count number
    """
    from robot.stupid import eval_holes
    board_t = array(board).T
    return eval_holes(board_t)


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
    for i in range(1, num_columns - 1):
        for j in range(0, len(board) - 1):
            if (not board[j][i]) and board[j][i - 1] and board[j][i + 1]:
                # Found well cell, count it + the number of empty cells below it.
                well_sums += 1

                for k in range(j + 1, len(board) - 1):  # ++k
                    if not board[k][i]:
                        well_sums += 1
                    else:
                        break

    # Check for well cells in the leftmost column of the board.
    for j in range(0, len(board) - 1):              # ++j
        if (not board[j][0]) and board[j][1]:
            # Found well cell, count it + the number of empty cells below it.
            well_sums += 1
            for k in range(j + 1, len(board) - 1):
                if not board[k][0]:
                    well_sums += 1
                else:
                    break

    # Check for well cells in the rightmost column of the board.
    for j in range(0, len(board) - 1):  # ++j
        if (not board[j][num_columns - 1]) and \
                board[j][num_columns - 2]:
            # Found well cell, count it + the number of empty cells below it.
            well_sums += 1
            for k in range(j + 1, len(board) - 1):  # ++k
                if not board[k][num_columns - 1]:
                    well_sums += 1
                else:
                    break
    return well_sums
