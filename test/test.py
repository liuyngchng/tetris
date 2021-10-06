# -*- coding:utf-8 -*-

import json

# import pdb;pdb.set_trace()
with open("data.json", "r", encoding='utf-8') as f:
    data = json.loads(f.read())
    print(data, type(data))
    print('score:', data['score'])
    print('ground:', data['ground'])
    a = [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ]

    b = [
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 0, 0, 0]
    ]
    print('a==b ?', a == b)

"""
    {
        'end_game': 0,
        'score': 100,
        'line_feed': 0,
        'ground':
            {'mat2d':
                 [
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                 ]
            },
        'spirit_this':
            {
                'x': 3,
                'y': -1,
                'type': 3,
                'rotate': 0,
                'mat2d':
                    [
                        [0, 0, 0, 0],
                        [0, 1, 1, 1],
                        [0, 1, 0, 0],
                        [0, 0, 0, 0]
                    ]},
        'spirit_next':
            {
                'type': 0,
                'rotate': 0,
                'mat2d':
                    [
                        [0, 0, 0, 0],
                        [0, 1, 1, 0],
                        [0, 1, 1, 0],
                        [0, 0, 0, 0]
                    ]
            }
"""