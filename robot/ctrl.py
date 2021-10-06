# -*- coding:utf-8 -*-
"""
controls game key and aim to get a high score
"""

from matrix import Matrix
from robot.ei import eval_grade_ei
from robot.ei_decimal import eval_grade_ei_decimal
from robot.stupid import eval_grade
from status import Status
from robot.motion import Motion
from copy import copy, deepcopy
from random import choice
import sys
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename=__name__+'.log')


class Ctrl:
    def __init__(self, motion: Motion):
        self.decision = None
        self.motion = motion

    def control(self, mtx_given: Matrix, status: Status, flag: int) -> None:
        """evaluate the final position where shape located in square,
        set the shape status (left, right, down) value, and move shape in GUI"""
        self.decision = make_decision(mtx_given, flag)
        # self.decision = ei.make_decision_ei(mtx_given)
        # logging.info("decision:\t%s", self.decision)
        set_shape_move_status(mtx_given, self.decision, status)
        data = self.move_gui_shape(status)
        # data = self.motion.apply()  # may be have lines full of points
        logging.info("score:\t%d", data['score'])
        result = self.fill_square_with_shape(mtx_given, data)
        return result

    def move_gui_shape(self, status: Status) -> dict:
        """move shape in GUI to the final position"""
        if status.rotate:
            self.gui_rotate()
        if status.left:
            self.gui_move_left()
        if status.right:
            self.gui_move_right()
        if status.down:
            # self.gui_drop_down()
            self.motion.apply()
        return self.motion.get_data()

    def gui_drop_down(self) -> int:
        old_data = None
        while old_data != self.decision['ul_corner'][0]:
            data = self.motion.down()
            old_data = self.motion.get_shape_info(data)['y']
        return old_data

    def gui_move_right(self) -> int:
        old_data = None
        while old_data != self.decision['ul_corner'][1]:
            data = self.motion.right()
            old_data = self.motion.get_shape_info(data)['x']
        return old_data

    def gui_move_left(self) -> int:
        old_data = None
        while old_data != self.decision['ul_corner'][1]:
            data = self.motion.left()
            old_data = self.motion.get_shape_info(data)['x']
        return old_data

    def gui_rotate(self) -> int:
        old_data = None
        while old_data != self.decision['rotate']:
            data = self.motion.rotate()
            old_data = self.motion.get_shape_info(data)['rotate']
        return old_data


    def fill_square_with_shape(self, mtx_given: Matrix, data: dict) -> bool:
        """
         fill the points in squares with solid points at the position assigned,
         and compare the data with gui square matrix 2d
        """
        for pos in self.decision['coordinates']:
            mtx_given.mat_data[pos[0]][pos[1]] = 1
        mtx_given.calc_clear_solid_rows()  # need to clean full lines to synchronize with GUI
        cmp_result = mtx_given.mat_data == data['ground']['mat2d']
        if not cmp_result:
            logging.error("error: squares calculated is not the same with GUI")
            sys.exit(-1)
        return cmp_result


def make_decision(mtx_given: Matrix, flag: int) -> dict:
    """return one direction to go"""
    mtx = copy_mtx(mtx_given)
    pos_data = get_possible_pos(mtx)
    """
    print(pos_data)
    [
        {'coordinates': [[18, 1], [19, 0], [19, 1], [19, 2]], 'ul_corner': [18, 0], 'rotate': 0}, 
        {'coordinates': [[18, 2], [19, 1], [19, 2], [19, 3]], 'ul_corner': [18, 1], 'rotate': 0}
    ]
    """
    eval_all_grade(mtx, pos_data, flag)
    return choose_pos(mtx, pos_data)


def choose_pos(mtx: Matrix, pos_data: list):
    """choose a position to drop down the shape"""
    while 1:
        top_level_pos = get_top_level(pos_data)
        try_result = try_choice(mtx, top_level_pos, pos_data)
        if try_result or len(pos_data) <= 1:
            break
    top_level_pos = get_top_level(pos_data)
    """
    return
    {'coordinates': [[18, 1], [19, 0], [19, 1], [19, 2]], 'ul_corner': [18, 0], 'rotate': 0}
    
    """
    return choice(top_level_pos)


def try_choice(mtx_given: Matrix, top_level_pos: dict, pos_data: list):
    """
         fill the points in squares with solid points at the position assigned,
         and compare the data with gui square matrix 2d
        """
    try_result = True
    mtx = copy_mtx(mtx_given)
    for pos in top_level_pos:
        for coordinate in pos['coordinates']:
            mtx.mat_data[coordinate[0]][coordinate[1]] = 1
        mtx.calc_clear_solid_rows()  # need to clean full lines to synchronize with GUI
        if assert_full(mtx, pos['coordinates'], mtx_given.mat_data):
            pos_data.remove(pos)    # pos is not Ok, try choice failed.
            try_result = False
    return try_result


def assert_full(mtx: Matrix, coordinates: list, mat_data_given: list):
    """assert if the matrix is full"""
    for row in mtx.mat_data:
        if sum(row):
            logging.error("_warning_:game over if choice %s used, discarded, mat_data:"
                          , coordinates)
            for idx, line in enumerate(mat_data_given):
                logging.error('%3d:\t%s', idx, line)
            return True
        else:
            return False


def eval_all_grade(mtx: Matrix, eval_data_list: list, flag: int) -> None:
    """
    put a grade for score for all the possible padding position
    """
    for eval_data in eval_data_list:
        pos = eval_data['coordinates']
        mtx_curr = copy_mtx(mtx)
        padding_matrix(mtx_curr, pos)
        # if flag == 0:
        #     eval_data['grade'] = eval_grade(mtx_curr)
        # elif flag == 1:
        eval_data['grade'] = eval_grade_ei(mtx_curr.mat_data, pos)
        # else :
        # eval_data['grade'] = eval_grade_ei_decimal(mtx_curr.mat_data, pos)
        # todo


def get_top_level(pos_data: dict) -> list:
    """highest marks might not be distinct, so return all of them"""
    # find highest score
    sort_key = lambda dict: dict['grade']
    max_data = max(pos_data, key=sort_key)
    max_grade = max_data['grade']
    # get all data with this mark
    all_highest = []
    for data in pos_data:
        if data['grade'] == max_grade:
            all_highest.append(data)
    return all_highest


def get_possible_pos(mtx_given: Matrix) -> list:
    """calculate all possible drop down position"""
    # copy given sqs for safety to calculate
    mtx_calc = copy_mtx(mtx_given)
    # reset rotation, curr = origin
    mtx_calc.curr_shape_mat2d = mtx_calc.origin_shape_mat2d
    mtx_calc.curr_rotate_index = mtx_calc.origin_rotate_index
    # generate position data
    pos = []
    for rotate_idx in range(mtx_calc.rotate_limit):
        mtx_calc.calc_shape_rotate(rotate_idx)
        balance_shape(pos, mtx_calc)
    return pos


def copy_mtx(mtx: Matrix) -> Matrix:
    """copy a matrix data structure safely"""
    mtx_copy = copy(mtx)
    mtx_copy.mat_data = deepcopy(mtx.mat_data)
    mtx_copy.curr_shape_pos = deepcopy(mtx.curr_shape_pos)
    return mtx_copy


def set_shape_move_status(mtx_given: Matrix, direction: dict, status: Status) -> None:
    """
    set shape move status before move shape in GUI
    direction = {'coordinates': [[17, 0], [16, 0], [15, 0], [18, 0]], 'center': [17, 0], 'rotate': 1, 'grade': 22.4875}
    """
    # rotation
    if mtx_given.origin_rotate_index != direction['rotate']:
        status.rotate = True
    else:
        status.rotate = False
    # move left horizontally
    if mtx_given.curr_shape_pos[1] > direction['ul_corner'][1]:
        status.left = True
    # move right horizontally
    elif mtx_given.curr_shape_pos[1] < direction['ul_corner'][1]:
        status.right = True
    # stop moving horizontally
    else:
        status.left = False
        status.right = False
    # move vertically
    if mtx_given.curr_shape_pos[0] != direction['ul_corner'][0]:
        status.down = True
    else:
        status.down = False


def balance_shape(pos: list, mtx: Matrix) -> None:
    """let shape rotate and move from left border to right border，and then drop down"""
    move_shape_to_left_border(mtx)
    old_pos = None
    # move from the left border to right border step by step
    # and record each position with drop to the end
    while old_pos != mtx.curr_shape_pos:
        mtx_curr = copy_mtx(mtx)
        mtx_curr.calc_shape_drop()
        record_curr_pos(pos, mtx_curr)
        old_pos = mtx.curr_shape_pos
        mtx.calc_shape_right()


def move_shape_to_left_border(mtx: Matrix) -> None:
    """move shape to left border"""
    old_pos = None  # to judge whether the shape next to the square border
    while old_pos != mtx.curr_shape_pos:
        old_pos = mtx.curr_shape_pos
        mtx.calc_shape_left()  # sqs.curr_shape_pos changed if not next to the border
    # logging.debug('sqs.squares:')


def record_curr_pos(pos: list, mtx: Matrix) -> None:
    """record all active squares"""
    all_point_pos = list()  # the coordinates of all point of shape in square
    y = mtx.curr_shape_pos[0]
    x = mtx.curr_shape_pos[1]
    for r_pos in mtx.new_shape['inner_pos'][mtx.curr_rotate_index]:
        all_point_pos.append([y + r_pos[0], x + r_pos[1]])
    pos.append({'coordinates': all_point_pos, 'ul_corner': mtx.curr_shape_pos, 'rotate': mtx.curr_rotate_index})
    # logging.debug(pos)


def padding_matrix(mtx: Matrix, positions: list) -> None:
    """
     padding the points which  position specified in matrix context
    """
    for pos in positions:
        mtx.mat_data[pos[0]][pos[1]] = 1
