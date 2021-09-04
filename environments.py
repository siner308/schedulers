#-*- coding: utf-8 -*-

from logger import get_my_logger


class Env:
    def __init__(self, filename):
        self.data = dict()
        self.get_envs(filename)

    def get_envs(self, filename):
        f = open(filename, 'r')
        while True:
            line = f.readline()
            if not line or line == '':
                break
            key_value = line.split('\n')[0].split('=')
            key = key_value[0]
            value = key_value[1]
            self.data['%s' % key] = value
        f.close()
