"""
duermevela-player main script.
"""


from pydub          import AudioSegment
from pydub.playback import play
from subprocess     import run
from time           import sleep


__version__ = '0.1.0'


def main():

    print(f"\nduermevela-player {__version__}: pydub test\n")

    print("loading 1000Hz test file... ", end='', flush=True)
    beep = AudioSegment.from_wav('data/1000Hz1s.wav')
    print('ok')
    sleep(1)

    print("playing file... ", end='', flush=True)
    play(beep)
    print("ok")
    sleep(1)

    print("looping and exporting... ", end='', flush=True)
    lupd = beep * 3
    lupd.export('var/sndtmp/lupd.wav', format='wav')
    lupd_read = AudioSegment.from_wav('var/sndtmp/lupd.wav')
    play(lupd_read)
    print('ok')
    sleep(1)
