"""
duermevela mecano parser and clock module.
"""

import json
import random

from dataclasses import dataclass

from duermevela.utils import alnum_only, cgtime2secs, letter_sum, note_freq, note_number


class Mecano:

    def __init__(self):

        with open(r"data/duermevela.json", encoding='utf-8') as f:
            data = json.load(f)
        self.previa   = data['previa']
        self.previa_s = cgtime2secs(self.previa)
        self.tocar    = data['tocar'].split()
        self.movts    = {n: Movt(*d) for n, d in data['movts'].items()}
        self.ngamuts  = {n: NGamut(d) for n, d in data['ngamuts'].items()}
        self.textes   = {n: Texte(d) for n, d in data['textes'].items()}

        with open(r"data/fieldrec.json", encoding='utf-8') as f:
            data = json.load(f)
        self.atisbos = [Atisbo(d, self) for d in data]


@dataclass
class Movt:
    label: str
    dur:   str

    def __post_init__(self):
        self.dur_s = cgtime2secs(self.dur)


@dataclass
class NGamut:
    _notes_str: str

    def __post_init__(self):
        self.notes = self._notes_str.split(" ")

    def frag(self, frag):
        """ find a fragment of the gamut, ie: mecano.ngamuts['landscape'].frag('3-5') = ["d2", "a2", "bb2"]. """

        start, end = frag.split("-") if "-" in frag else (frag, frag)
        return self.notes[(int(start) - 1):int(end)]


@dataclass
class Texte:
    lines: list

    def frag(self, frag, first_verse=False):
        """ find a fragment of the texte, ie: mecano.textes['satie'].frag('15-16') = "que nadie nunca". """

        start, end = frag.split("-") if "-" in frag else (frag, frag)
        if first_verse:
            end = start
        return " ".join(self.lines[(int(start) - 1):int(end)])


class Atisbo:

    def __init__(self, atisbo, mecano):

        self._atisbo     = atisbo
        # {"mom":   [79, "v", "1'51", "2'59", "6'31"],
        #  "texte": ["satie", "27", 2],
        #  "modos": ["nl", "al", "pu", "bc"],
        #  "ng":    ["landscape", "8-15", 8],
        #  "dyn":   ["pppp", "<>"]}

        self.movt        = self._atisbo['mom'][1]

        self.start1      = self._atisbo['mom'][2]
        self.start1_s    = cgtime2secs(self.start1)
        self.start2      = self._atisbo['mom'][3]
        self.start2_s    = cgtime2secs(self.start2)
        self.movt_end    = self._atisbo['mom'][4]
        self.movt_end_s  = cgtime2secs(self.start2)

        self.texte       = mecano.textes[self._atisbo['texte'][0]].frag(self._atisbo['texte'][1]).strip()
        self.texte_words = alnum_only(self.texte, keep_spaces=True).split()
        self.texte_alnum = alnum_only(self.texte)
        self.texte_count = len(self.texte_alnum)
        self.texte_sum   = letter_sum(self.texte_alnum)

        self.verse       = mecano.textes[self._atisbo['texte'][0]].frag(self._atisbo['texte'][1], first_verse=True)
        self.verse_words = alnum_only(self.verse, keep_spaces=True).split()
        self.verse_alnum = alnum_only(self.verse)
        self.verse_count = len(self.verse_alnum)
        self.verse_sum   = letter_sum(self.verse_alnum)

        self.words       = " ".join(self.texte_words[:3])
        self.words_words = alnum_only(self.words, keep_spaces=True).split()
        self.words_alnum = alnum_only(self.words)
        self.words_count = len(self.words_alnum)
        self.words_sum   = letter_sum(self.words_alnum)

        self.modo        = random.choice(self._atisbo['modos'])

        self.notes       = mecano.ngamuts[self._atisbo['ng'][0]].frag(self._atisbo['ng'][1])
        self.note_freqs  = [note_freq(n) for n in self.notes]
        self.note_nums   = [note_number(n) for n in self.notes]

        self.dyn_max     = self._atisbo['dyn'][0]
        self.dyn_shape   = self._atisbo['dyn'][1]
