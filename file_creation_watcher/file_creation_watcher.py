import time

from watchdog.observers import Observer


class FileCreationWatcher:
    def __init__(self):
        self.__src_path = '/mnt/file-store/'
        self.__event_handler = FileCreationEvent()
        self.__event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                time.sleep(60)
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


class FileCreationEvent:
    def __init__(self):
        print('hi there')


if __name__ == "__main__":
    FileCreationWatcher().run()
