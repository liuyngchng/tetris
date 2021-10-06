# -*- coding:utf-8 -*-
from numpy import array, mean
from config import Config
from matrix import Matrix

cfg = Config()


def eval_grade(mtx: Matrix) -> float:
    """get the features of the square , and calculate a final score"""
    solid_rows = get_solid_rows(mtx)
    mtx.calc_clear_solid_rows()
    matrix_t = array(mtx.mat_data).T  # convert rows to columns
    holes = eval_holes(matrix_t)
    min_col_high, avg_col_high, col_high_diff = eval_column(matrix_t)
    return put_grade(solid_rows, holes, min_col_high, avg_col_high, col_high_diff)


def get_solid_rows(mtx: Matrix) -> int:
    """after shape drop down，count the line fulling of solid points"""
    solid_rows = 0
    for row in mtx.mat_data:
        if row.count(0) == 0:
            solid_rows += 1
    return solid_rows


def eval_holes(mtx_t: list) -> int:
    """find the number of non-squares under squares"""
    holes = 0
    for column in mtx_t:
        solid_point_found = False
        for point in column:
            # find first square
            if not solid_point_found:
                if point != 0:
                    solid_point_found = True
                else:
                    continue
            # find hidden squares
            if point == 0:
                holes += 1
    return holes


def eval_column(mtx_t: list) -> tuple:
    """count lowest and average space left in every column"""
    hollow_col_high = []  # the high(in y axis) of the hollow column on top of the solid column.
    for col in mtx_t:
        appended = False
        for idx, point in enumerate(col):
            # check every point
            if point != 0:  # the first solid point is the end of the hollow column
                hollow_col_high.append(idx)
                appended = True
                break
        if not appended:
            hollow_col_high.append(len(col))  # the overall column is hollow
    return min(hollow_col_high), mean(hollow_col_high), max(hollow_col_high) - min(hollow_col_high)


#
def put_grade(solid_rows: int, holes: int, min_col_high: int, avg_col_high: int, col_high_diff: int) -> float:
    """put grade for scores to the context matrix
    """
    grade = 0
    grade += solid_rows * cfg.solid_row_weight
    grade += holes * cfg.hole_weight
    grade += min_col_high * cfg.min_col_high_weight
    grade += avg_col_high * cfg.avg_col_high_weight
    grade += col_high_diff * cfg.high_diff_weight
    return grade
