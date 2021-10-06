# -*- coding:utf-8 -*-

from config import Config
from matrix import Matrix
from robot.ctrl import Ctrl, make_decision
from robot.motion import Motion
from status import Status

if __name__ == '__main__':
    cfg = Config()
    motion = Motion(cfg.base_url)
    status = Status()
    ctrl = Ctrl(motion)
    matrix = Matrix(cfg, status, motion)          # create instance of matrix
    # new data
    matrix.mat_data = [
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ] ,
        [ 0, 0, 0, 0, 0, 1, 0, 0, 1, 0 ] ,
        [ 0, 0, 0, 0, 1, 1, 1, 1, 1, 1 ] ,
        [ 0, 0, 0, 0, 1, 1, 1, 1, 1, 1 ] ,
        [ 0, 0, 0, 0, 1, 1, 1, 1, 1, 1 ]
    ]
    # new data
    matrix.shape_info = {
        "x": 3, "y": -1,
        "type": 1, "rotate": 0,
        "mat2d": [
            [ 0, 0, 0, 0 ] ,
            [ 1, 1, 1, 1 ] ,
            [ 0, 0, 0, 0 ] ,
            [ 0, 0, 0, 0 ]
        ]

    }
    matrix.shape_type = matrix.shape_info['type']
    matrix.origin_shape_mat2d = matrix.shape_info['mat2d']  # shape的mat2d，计算旋转时不变
    matrix.curr_shape_mat2d = matrix.origin_shape_mat2d.copy()  # shape的mat2d，计算图形旋转时改变

    # new shape data
    matrix.new_shape = matrix.get_shape()
    matrix.rotate_limit = matrix.new_shape['rotate']
    matrix.origin_rotate_index = matrix.new_shape['rotate_index']  # 图形旋转后改变
    matrix.curr_rotate_index = matrix.origin_rotate_index  # 计算旋转时的逻辑旋转数据
    matrix.status.reset()
    ctrl.control(matrix, status, 1)
