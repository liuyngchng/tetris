# -*- coding:utf-8 -*-


class Config:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000/'
        # warning: shapes, dont touch this if you are not clear about what this dose
        # inner_pos, coordinate illustrated in form (y, x), all points in shape（4*4 matrix）
        # located corresponding to left upper corner (0,0)
        self.shapes = (
            {'inner_pos': [
                    [(0, 1), (1, 0), (1, 1), (1, 2)],
                    [(0, 1), (1, 1), (1, 2), (2, 1)],
                    [(1, 0), (1, 1), (1, 2), (2, 1)],
                    [(0, 1), (1, 0), (1, 1), (2, 1)]
                 ],
             'rotate': 4, 'type': 2, 'rotate_index': 0,
             'shape': [
                 [
                     [0, 1, 0, 0],
                     [1, 1, 1, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0]
                 ],
                 [
                     [0, 1, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]
                 ],
                 [
                     [0, 0, 0, 0],
                     [1, 1, 1, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]
                 ],
                 [
                     [0, 1, 0, 0],
                     [1, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 0]
                 ]
             ]
             },  # _|_
            {'inner_pos': [
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)],
                [(1, 1), (1, 2), (2, 1), (2, 2)]
            ],
             'rotate': 4, 'type': 0, 'rotate_index': 0,
             'shape': [
                 [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0]
                 ],
                 [
                     [0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]
                 ],
                 [
                     [0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]
                 ],
                 [
                     [0, 0, 0, 0],
                     [0, 1, 1, 0],
                     [0, 1, 1, 0],
                     [0, 0, 0, 0]
                 ]
             ]
             },  # ::
            {'inner_pos': [
                [(1, 0), (1, 1), (1, 2), (1, 3)],
                [(0, 2), (1, 2), (2, 2), (3, 2)],
                [(2, 0), (2, 1), (2, 2), (2, 3)],
                [(0, 1), (1, 1), (2, 1), (3, 1)]
            ],
             'rotate': 4, 'type': 1, 'rotate_index': 0,
             'shape': [
                 [
                    [0, 0, 0, 0],
                    [1, 1, 1, 1],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0]
                 ],

                [
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0],
                    [0, 0, 1, 0]
                 ],
                 [
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [1, 1, 1, 1],
                     [0, 0, 0, 0]
                 ],
                 [
                     [0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 0, 0],
                     [0, 1, 0, 0]
                 ]
             ]
             }  # |
        )

        self.shape_num = len(self.shapes)           # 下落图形的数量

        # positions
        self.square_num_x = 10                      # 屏幕宽度的方格数
        self.square_num_y = 20                      # 屏幕高度的方格数

        # 新出现的形状所在位置坐标
        self.new_shape_pos = []                               # 新出现图形的坐标

        """
       (1)solid_row: the number of the row count with all solid points
       (2)holes: the number of hollow points under solid points
       (3)min_col_high: the smallest high of the whole hollow column on the top
       (4)avg_col_high: the average high of the whole hollow column on the top
       (5)col_high_diff: the maximum high difference among all hollow columns ton the top
       (6)arguments weight, set manually based on experiment
       """
        self.solid_row_weight = 20
        self.hole_weight = -2
        self.min_col_high_weight = 0.3
        self.avg_col_high_weight = 0.15
        self.high_diff_weight = -1