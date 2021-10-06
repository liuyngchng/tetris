# -*- coding:utf-8 -*-
import requests
import json

s = requests.Session()


def req(url: str) -> dict:
    resp = s.get(url)
    data = json.loads(resp.content)
    return data


class Motion:
    def __init__(self, url):
        self.base_url = url
        self.data_url = self.base_url + 'data'
        self.left_url = self.base_url + 'left'
        self.right_url = self.base_url + 'right'
        self.rotate_url = self.base_url + 'rotate'
        self.down_url = self.base_url + 'down'
        self.apply_url = self.base_url + 'apply'
        self.reset_url = self.base_url + 'reset_all'

    def left(self) -> dict:
        """move shape left in GUI"""
        return req(self.left_url)

    def right(self) -> dict:
        """move shape right in GUI"""
        return req(self.right_url)

    def down(self) -> dict:
        """move down left in GUI"""
        return req(self.down_url)

    def rotate(self) -> dict:
        """rotate shape left in GUI"""
        return req(self.rotate_url)

    def apply(self) -> dict:
        """balance the score and create a new shape in GUI"""
        return req(self.apply_url)

    def reset_all(self) -> dict:
        """reset game in GUI"""
        return req(self.reset_url)

    def get_data(self) -> dict:
        """get data of the current state in GUI"""
        return req(self.data_url)

    @staticmethod
    def get_curr_shape() -> dict:
        """
        get the current shape info in GUI, for test purpose only
        :return: {
            "x": 3,
            "y": -1,
            "type": 2,
            "rotate": 0,
            "mat2d": [
              [0, 1, 0, 0],
              [1, 1, 1, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]
            ]
          }
        """
        return {
            "x": 3,
            "y": -1,
            "type": 2,
            "rotate": 0,
            "mat2d": [
                [0, 1, 0, 0],
                [1, 1, 1, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0]
            ]
        }

    @staticmethod
    def get_shape_info(data: dict) -> dict:
        """get shape info from GUI"""
        return data['spirit_this']


if __name__ == "__main__":
    motion = Motion()
    # import pdb
    # pdb.set_trace()
    print(motion.get_data())
