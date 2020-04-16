import time

import requests
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class FileCreationWatcher:
    def __init__(self):
        self.src_path = '/mnt/file-store/'
        self.event_handler = FileCreationEvent()
        self.event_observer = Observer()

    def run(self):
        self.start()
        try:
            while True:
                print('Checking...')
                time.sleep(30)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        self.schedule()
        self.event_observer.start()

    def stop(self):
        self.event_observer.stop()
        self.event_observer.join()

    def schedule(self):
        self.event_observer.schedule(
            self.event_handler,
            self.src_path,
            recursive=True
        )


class FileCreationEvent(PatternMatchingEventHandler):
    def __init__(self):
        super(FileCreationEvent, self).__init__()
        self._ignore_directories = True
        self._patterns = 'random_numbers-*'

    def on_created(self, event):
        print('EVENT INCOMING!')
        print(event.src_path)
        r = requests.post(
            'http://airflow-web.airflow.svc.cluster.local:8080/api/experimental/dags/random_number_watcher/dag_runs',
            json={"conf": {"file_path": event.src_path}}
        )
        print(r.status_code, r.reason)


if __name__ == "__main__":
    FileCreationWatcher().run()
