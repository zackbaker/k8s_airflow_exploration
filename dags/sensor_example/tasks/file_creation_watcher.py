import json
import time
import logging

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class FileCreationWatcher:
    def __init__(self):
        self.__src_path = '/mnt/file-store/'
        self.__event_handler = FileCreationEvent()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                logging.info('Checking...')
                time.sleep(30)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.__schedule()
        self.__event_observer.start()

    def stop(self):
        self.__event_observer.stop()
        self.__event_observer.join()

    def __schedule(self):
        self.__event_observer.schedule(
            self.__event_handler,
            self.__src_path,
            recursive=True
        )


class FileCreationEvent(PatternMatchingEventHandler):
    def __init__(self):
        super(FileCreationEvent, self).__init__()
        self._ignore_directories = True
        self._patterns = 'random_numbers-*'

    def on_created(self, event):
        logging.info('EVENT INCOMING!')
        logging.info(event.src_path)
        with open('/airflow/xcom/return.json', 'w') as outfile:
            json.dump(event, outfile)
        exit(0)


if __name__ == "__main__":
    FileCreationWatcher().run()
