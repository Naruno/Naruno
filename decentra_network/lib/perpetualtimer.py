#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from threading import Event, Thread, Timer


class perpetualTimer(Timer):
    """
    It trig the functions at time intervals, independent of the main process.

    perpetualTimer class consists of 3 elements:
      * t: The time interval of perpetualTimer.
      * hFunction: The function to be triggered.
    """

    def __init__(self, interval, function, args=None, kwargs=None):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = Event()

        if self.interval != 0:
            self.start()

    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)