#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
from threading import Thread

import kivy
from kivy.app import App
from kivy.uix.label import Label

from decentra_network.api.main import start


class Decentra_Network_API(App):

    def build(self):
        the_api = Thread(target=start)
        the_api.start()
        return Label(text="Decentra-Network-API")


if __name__ == "__main__":
    Decentra_Network_API().run()
