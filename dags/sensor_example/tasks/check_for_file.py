import logging
import pyinotify


def run():
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, trigger_dag())
    wm.add_watch('/mnt/file-store', pyinotify.CREATE)
    notifier.loop()


def trigger_dag():
    logging.info('We have found a File!')


if __name__ == '__main__':
    run()
