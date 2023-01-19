#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time

from kivy.app import App
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

from decentra_network.lib.settings_system import d_mode_settings
from decentra_network.lib.settings_system import dark_mode_settings
from decentra_network.lib.settings_system import mt_settings
from decentra_network.lib.settings_system import t_mode_settings
from decentra_network.lib.settings_system import the_settings


class SettingsScreen(MDScreen):
    pass


class SettingsBox(MDGridLayout):
    cols = 2

    d_first_status = the_settings()["debug_mode"]
    t_first_status = the_settings()["test_mode"]
    mt_first_status = the_settings()["mute_notifications"]
    dark_mode_first_status = the_settings()["dark_mode"]

    def D_Status_Changing(self, instance, value):
        d_mode_settings(value)

    def T_Status_Changing(self, instance, value):
        t_mode_settings(value)

    def MT_Status_Changing(self, instance, value):
        mt_settings(value)

    def show_dialog(self):
        button_ok = MDRaisedButton(
            text="OK",
            font_size=16,
            on_release=self.callback,
        )
        button_cancel = MDFlatButton(
            text="CANCEL",
            font_size=16,
            on_release=self.callback,
        )
        self.alert = SweetAlert()
        self.alert.fire(
            "The app will restart.",
            buttons=[button_ok, button_cancel],
            type="info",
        )

    def callback(self, instance_button):
        if instance_button.text == "OK":
            self.alert.dismiss()
            SettingsBox.dark_mode_first_status = the_settings()["dark_mode"]
            App.get_running_app().restart()

        else:
            self.alert.dismiss()

    def DARK_MODE_Status_Changing(self, instance, value):

        dark_mode_settings(value)
        self.show_dialog()
