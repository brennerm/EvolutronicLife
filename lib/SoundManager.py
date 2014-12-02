from threading import Thread
from subprocess import Popen, PIPE


class SoundManager(Thread):
    def __init__(self, background_sound):
        super(SoundManager, self).__init__()
        self._background_sound = background_sound
        self._process = None

    def run(self):
        if not self._background_sound is None:
            self._process = Popen(['cvlc', '-R', self._background_sound], stdout=PIPE, stderr=PIPE)

    def terminate(self):
        if not self._process is None:
            self._process.terminate()