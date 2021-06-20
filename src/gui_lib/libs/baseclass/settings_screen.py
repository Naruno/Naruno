#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

from lib.settings_system import the_settings, test_mode, debug_mode


class SettingsScreen(MDScreen):
    pass

class SettingsBox(MDGridLayout):
    cols = 2
    d_first_status = the_settings()["debug_mode"]
    t_first_status = the_settings()["test_mode"]



    def D_Status_Changing(self, instance, value):
        debug_mode(value)

    def T_Status_Changing(self, instance, value):
        test_mode(value)
