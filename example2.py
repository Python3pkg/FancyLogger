#!/bin/env/python
# coding: utf-8

import os
import time
from multiprocessing import Process
from random import randrange

from FancyLogger import FancyLogger, TaskProgress


def pid(text):
    return '[{}] : {}'.format(os.getpid(), text)


class WorkerClass(Process):

    def __init__(self, logger):
        super(WorkerClass, self).__init__()

        self.logger = logger

        # Define a random progress bar
        self.enumerable_data = range(randrange(50, 500))

    def run(self):
        self.logger.info(pid('Hello there :)'))

        # Here we simulate some work using a progress bar iterator
        for _ in self.logger.progress(enumerable=self.enumerable_data,
                                      task_progress_object=TaskProgress(total=None,  # Total is computed by iterator
                                                                        prefix=pid('Progress'),
                                                                        keep_alive=False,
                                                                        display_time=True)):
            time.sleep(.01)

        self.logger.info(pid('See you later!'))


class App(object):

    def __init__(self):
        super(App, self).__init__()

    @classmethod
    def example(cls):

        # Configure and start the logger process
        logger = FancyLogger(permanent_progressbar_slots=9)

        # Create a random list of worker processes
        workers = [WorkerClass(logger) for _ in range(randrange(5, 10))]

        logger.info('[main] : Start processing things')

        # Start processes
        for w in workers:
            w.start()

        # Wait for processes one by one, using a progress bar iterator for the main thread
        for w in logger.progress(enumerable=workers,
                                 task_progress_object=TaskProgress(total=None,  # Total is computed by iterator
                                                                   prefix='Main task',
                                                                   keep_alive=True)):
            w.join()

        logger.info('[main] : End of processing ({} objects)'.format(len(workers)))

        # Display log messages and progress bars as they are right now, to see their last state before exiting
        # Indeed the logger uses a refresh rate that can be set during initialization. If you do not call flush method
        # then you might miss the last messages and progress bar states that have not been displayed yet
        logger.flush()
        # Stop the logger process
        logger.terminate()

if __name__ == '__main__':
    App.example()
