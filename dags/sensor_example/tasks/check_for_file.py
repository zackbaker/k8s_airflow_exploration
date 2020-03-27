import logging
import pyinotify


def run(ds, **kwargs):
    wm = pyinotify.WatchManager()
    notifier = pyinotify.Notifier(wm, trigger_dag(ds, kwargs))
    wm.add_watch('/mnt/file-store', pyinotify.CREATE)
    notifier.loop()


def trigger_dag(ds, kwargs):
    logging.info('We have found a File!')


if __name__ == '__main__':
    run()
