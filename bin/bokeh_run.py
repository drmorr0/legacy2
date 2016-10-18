#!/usr/bin/env python

import os
import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BokehRestartEventHandler(FileSystemEventHandler):

    def __init__(self):
        self.process = subprocess.Popen('bokeh serve legacy'.split(), stdout=subprocess.PIPE)
        self.last_restart = time.time()

    def _del__(self):
        self.process.kill()

    def on_any_event(self, event):
        extension = os.path.splitext(event.src_path)
        if extension[1] not in ['.py', '.js', '.html']:
            return

        if time.time() < self.last_restart + 5:
            return

        print("Restarting bokeh server")
        self.process.kill()
        self.process = subprocess.Popen('bokeh serve legacy'.split(), stdout=subprocess.PIPE)
        self.last_restart = time.time()


if __name__ == '__main__':

    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    handler = BokehRestartEventHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    del handler
