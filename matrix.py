# -*- coding:utf-8 -*-

from robot.motion import Motion
from config import Config
from status import Status
import logging

# logging.basicConfig函数对日志的输出格式及方式做相关配置
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename='./log/'+__name__+'.log')


class Matrix:
    """manipulating shapes in squares for evaluation purpose only"""

    def __init__(self, cfg: Config, status: Status, motion: Motion):
        self.cfg = cfg
        self.motion = motion
        self.status = status
        self.empty_line = [0 for i in range(cfg.square_num_x)]   # one line in square, init
        self.mat_data = self.motion.get_data()['ground']['mat2d']     # y*x square matrix init
        # new shape coordinates，all coordinates illustrated in form [y,x]
        self.origin_shape_pos = self.cfg.new_shape_pos   # shape rotated but shape pos does not change
        self.update()                                   # some init need to be done in turn when new shape created
        self.origin_shape_pos.append(self.shape_info['y'])      # y axis
        self.origin_shape_pos.append(self.shape_info['x'])      # origin_shape_pos = [y, x]

        logging.info("self.origin_shape_pos:%s", self.origin_shape_pos)
        self.curr_shape_pos = self.origin_shape_pos.copy()      # logic position of shape in evaluation, [y, x]

    def update(self) -> None:
        """update square's information for next iteration"""
        self.shape_info = self.motion.get_shape_info(self.motion.get_data())  # 在线获取, 计算旋转过程中不变
        self.shape_type = self.shape_info['type']
        self.origin_shape_mat2d = self.shape_info['mat2d']  # shape的mat2d，计算旋转时不变
        self.curr_shape_mat2d = self.origin_shape_mat2d.copy()  # shape的mat2d，计算图形旋转时改变

        # new shape data
        self.new_shape = self.get_shape()
        self.rotate_limit = self.new_shape['rotate']
        self.origin_rotate_index = self.new_shape['rotate_index']  # 图形旋转后改变
        self.curr_rotate_index = self.origin_rotate_index  # 计算旋转时的逻辑旋转数据
        self.status.reset()

    def get_shape(self) -> None:
        """find the corresponding data dictionary"""
        for shape in self.cfg.shapes:
            if shape['type'] == self.shape_type:
                return shape
        logging.error("error occurred in get_shape")
        return None

    def calc_shape_drop(self) -> None:
        """shape drop down in square"""
        yx_matrix = self.calc_shape_coordinate_range()  # shape (y, x) coordinate range in square

        # find the lowest position y_offset which used to calculate y coordinate
        flag = False                                # flag for finish to found max_hollow_line
        max_hollow_line = 0                         # max hollow line which shape can drop to
        for y in range(self.cfg.square_num_y):       # max value 'square_num_y' not include
            max_hollow_line = y
            for x in range(yx_matrix[1][0], yx_matrix[1][1] + 1):  # max value 'x_range[1] + 1' not include
                if self.mat_data[y][x]:              # line in square with solid point
                    max_hollow_line = y - 1
                    flag = True
                    break
                else:
                    continue
            if flag:
                break

        # logging.debug('max_hollow_line = %d', max_hollow_line)
        # TODO debug
        # move straight
        self.curr_shape_pos[0] = max_hollow_line - len(self.curr_shape_mat2d) + 1  # change shape coordinate y
        # move down carefully step by step
        old_pos = None
        while old_pos != self.curr_shape_pos:
            old_pos = self.curr_shape_pos
            self.calc_shape_down()
        # refresh the square data.
        for i in range(len(self.curr_shape_mat2d)):
            for j in range(len(self.curr_shape_mat2d[0])):
                if self.curr_shape_mat2d[i][j]:
                    y = self.curr_shape_pos[0] + i
                    x = self.curr_shape_pos[1] + j
                    self.mat_data[y][x] = 1
        # logging.debug("self.squares after shape drop down:")
        # for i, row in enumerate(self.squares):
        #     if sum(row):
        #         logging.debug('%d\t%s', i, row)
        # logging.debug("shape pos:(%d, %d)",
        #               self.curr_shape_pos[1],
        #               self.curr_shape_pos[0])

    def calc_shape_coordinate_range(self) -> list:
        """calculate the coordinate range of shape in square"""
        y_range = [self.curr_shape_pos[0],  # y coordinate of current shape in square
                   self.curr_shape_pos[0] + len(self.curr_shape_mat2d) - 1]  # [min, max]
        x_range = [self.curr_shape_pos[1],
                   self.curr_shape_pos[1] + len(self.curr_shape_mat2d[0]) - 1]  # [min, max]
        # the coordinates of hollow points in curr_shape_mat2d may be not in range of square context，
        # but the solid points must be in the range of square
        if y_range[0] < 0:
            y_range[0] = 0
        if y_range[1] > self.cfg.square_num_y - 1:
            y_range[1] = self.cfg.square_num_y - 1
        if x_range[0] < 0:
            x_range[0] = 0
        if x_range[1] > self.cfg.square_num_x - 1:
            x_range[1] = self.cfg.square_num_x - 1
        return [y_range, x_range]

    def calc_shape_down(self) -> None:
        """move shape down by 1 unit"""
        new_shape_pos = self.curr_shape_pos.copy()
        new_shape_pos[0] += 1                          # in form [y, x]
        if self.validate_shape(new_shape_pos):
            self.curr_shape_pos = new_shape_pos        # update shape position

    def calc_shape_rotate(self, rotate_idx: int) -> None:
        """do not make shape rotated in GUI，just for evaluation"""
        self.curr_rotate_index = rotate_idx
        # update current shape mat2d
        self.curr_shape_mat2d = self.get_shape().get('shape')[self.curr_rotate_index]
        # logging.debug("self.curr_shape_mat2d:")
        # for line in self.curr_shape_mat2d:
        #     logging.debug(line)

    def calc_shape_right(self) -> None:
        """move shape to right by 1 unit"""
        new_shape_pos = self.curr_shape_pos.copy()
        new_shape_pos[1] += 1
        if self.validate_shape(new_shape_pos):
            self.curr_shape_pos = new_shape_pos

    def calc_shape_left(self) -> None:
        """move shape to left by 1 unit"""
        new_shape_pos = self.curr_shape_pos.copy()
        new_shape_pos[1] -= 1  # [y, x]
        if self.validate_shape(new_shape_pos):
            self.curr_shape_pos = new_shape_pos  # update shape position

    def calc_clear_solid_rows(self) -> int:
        """delete lines fulling of solid points and insert empty lines at the top of the square
        return the line count which fulling of solid points
        """
        solid_rows = 0
        for index, row in enumerate(self.mat_data):
            if row.count(0) == 0:
                solid_rows += 1
                self.mat_data.pop(index)  # remove line full of solid points
                self.mat_data.insert(0, self.empty_line.copy())  # insert a new line instead
        return solid_rows

    def validate_shape(self, new_shape_pos: list) -> bool:
        """校验new_shape_pos是否在有效坐标范围内（边界检查）,
        同时不与已有的背景square发生冲突"""
        result = True
        # check shape mat2d
        for i in range(len(self.curr_shape_mat2d)):
            for j in range(len(self.curr_shape_mat2d[0])):
                if not self.curr_shape_mat2d[i][j]:  # hollow point
                    continue
                # position of the solid points in shape
                y = new_shape_pos[0] + i  # [y, x]
                x = new_shape_pos[1] + j
                # border check
                if x < 0 or x >= self.cfg.square_num_x \
                        or y < -2 or y >= self.cfg.square_num_y:
                    return False
                # new shape collision detection with context square mat2d
                # curr_shape_mat2d 中的 hollow point 的坐标（y,x）可以超出square的坐标范围，
                # 但 solid point的坐标(y,x)必须在square的坐标范围内,
                # solid point 在gui中有小于0的情况，需要排除
                if y >= 0 and self.mat_data[y][x]:
                    return False
        return result
