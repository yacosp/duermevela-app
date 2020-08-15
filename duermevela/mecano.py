"""
duermevela mecano parser and clock module.
"""

import json

from collections import namedtuple

from .utils import cgtime2secs, secs2cgtime


class Mecano:

    def __init__(self):

        with open(r"data/duermevela.json") as f:
            data = json.load(f)
        self.previa = data['previa']
        self.previa_s = cgtime2secs(self.previa)
        self.tocar = data['tocar']
        self.movts = data['movts']
        self.ng = data['ng']

        with open(r"data/fieldrec.json") as f:
            self.mecano = json.load(f)


class MovtTuple(namedtuple('MovtTuple', ['name', 'label', 'dur'])):

    @property
    def dur_s(self):
        return cgtime2secs(self.dur)
