from PySide import QtGui, QtCore
import sys
import threading
import time
import unittest


class ThreadIter(QtCore.QObject):
    _fireCallback = QtCore.Signal(unicode)

    def __init__(self, iterable, cb):
        QtCore.QObject.__init__(self)
        self.iterable = iterable
        self._fireCallback.connect(cb)

        def make_thread():
            th = threading.Thread(target=self._run_thread)
            th.daemon = True
            th.start()
            return th
        self.thread = make_thread()

    def _run_thread(self):
        for item in self.iterable:
            self._fireCallback.emit(item)


def yielder():
    for e in range(10):
        # Pretend to be an expensive file operation
        # by sleeping between yields
        time.sleep(0.1)
        yield str(e)


class TestStartsUp(unittest.TestCase):
    def testStartsUp(self):
        QtGui.QApplication([])
        ThreadIter(yielder(), cb=lambda: None)


def main():
    app = QtGui.QApplication(sys.argv)
    widg = QtGui.QListWidget()
    widg.show()

    def cb(item):
        widg.addItem(item)
    ThreadIter(yielder(), cb)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
