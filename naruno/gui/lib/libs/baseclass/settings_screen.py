#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import shutil
import time

from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.utils import platform
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

import naruno.gui.the_naruno_gui_app
from naruno.gui.popup import popup
from naruno.lib.backup.naruno_export import naruno_export
from naruno.lib.backup.naruno_import import naruno_import
from naruno.lib.settings_system import d_mode_settings
from naruno.lib.settings_system import dark_mode_settings
from naruno.lib.settings_system import mt_settings
from naruno.lib.settings_system import t_mode_settings
from naruno.lib.settings_system import the_settings
from naruno.lib.settings_system import baklava_settings


class SettingsScreen(MDScreen):
    pass


class SettingsBox(MDGridLayout):
    cols = 2

    d_first_status = the_settings()["debug_mode"]
    t_first_status = the_settings()["test_mode"]
    mt_first_status = the_settings()["mute_notifications"]
    dark_mode_first_status = the_settings()["dark_mode"]
    baklava_first_status = the_settings()["baklava"]

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
            naruno.gui.the_naruno_gui_app.the_naruno_gui.restart()

        else:
            self.alert.dismiss()

    def DARK_MODE_Status_Changing(self, instance, value):
        dark_mode_settings(value)
        self.show_dialog()

    def BAKLAVA_Status_Changing(self, instance, value):
        baklava_settings(value)


    def export_bt(self):
        export_location = naruno_export()
        Clipboard.copy(export_location)
        if platform == "android":
            from android.storage import primary_external_storage_path

            dir = primary_external_storage_path()
            download_dir_path = os.path.join(dir, "Download")
            new_path = os.path.join(download_dir_path,
                                    export_location.split("/")[-1])
            Clipboard.copy(new_path)
            shutil.move(
                export_location,
                new_path,
            )
        popup(
            title="The export file location has been copied to your clipboard.",
            type="success",
        )

    def import_the_db(self):
        naruno_import(self.import_backup_dialog.input_results["Path"])
        SettingsBox.dark_mode_first_status = the_settings()["dark_mode"]
        SettingsBox.d_first_status = the_settings()["debug_mode"]
        SettingsBox.t_first_status = the_settings()["test_mode"]
        SettingsBox.mt_first_status = the_settings()["mute_notifications"]
        SettingsBox.baklava_first_status = the_settings()["baklava"]
        naruno.gui.the_naruno_gui_app.the_naruno_gui.restart()

    def import_bt(self):
        self.import_backup_dialog = popup(
            title="Import your export (App Will Restart)",
            target=self.import_the_db,
            inputs=[["Path", False]],
        )
