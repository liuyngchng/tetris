#!/usr/bin/python3
# -*- coding:utf-8 -*-

from robot.motion import Motion
from config import Config
from robot.ctrl import Ctrl
from status import Status
from matrix import Matrix
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='./log/'+__name__+'.log')

if __name__ == "__main__":
    # import pdb;pdb.set_trace()
    flag = 1
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    cfg = Config()
    motion = Motion(cfg.base_url)
    motion.reset_all()
    motion.apply()
    status = Status()
    ctrl = Ctrl(motion)
    matrix = Matrix(cfg, status, motion)          # create instance of matrix
    logging.debug("sqs=%s", matrix)
    data = motion.get_data()
    turn = 0
    while data['end_game'] == 0:
        logging.info("turn:\t%d", turn)
        ctrl.control(matrix, status, flag)
        data = motion.get_data()
        matrix.update()
        turn += 1
    logging.info("final score is:\t%d", data['score'])
