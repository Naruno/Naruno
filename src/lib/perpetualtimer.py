#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


from threading import Timer


class perpetualTimer:
    """
    It trig the functions at time intervals, independent of the main process.

    perpetualTimer class consists of 3 elements:
      * t: The time interval of perpetualTimer.
      * hFunction: The function to be triggered.
      * thread: The threading timer function.
    """

    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        """
        Runs the function.
        """

        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        """
        Cancels the perpetualTimer.
        """

        self.thread.start()

    def cancel(self):
        """
        Cancels the perpetualTimer.
        """

        self.thread.cancel()
