#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

from decentra_network.lib.settings_system import d_mode_settings
from decentra_network.lib.settings_system import t_mode_settings
from decentra_network.lib.settings_system import the_settings


class SettingsScreen(MDScreen):
    pass


class SettingsBox(MDGridLayout):
    cols = 2
    d_first_status = the_settings()["debug_mode"]
    t_first_status = the_settings()["test_mode"]

    def D_Status_Changing(self, instance, value):
        d_mode_settings(value)

    def T_Status_Changing(self, instance, value):
        t_mode_settings(value)
