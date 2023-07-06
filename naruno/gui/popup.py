#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os

from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd_extensions.sweetalert import SweetAlert

import naruno.gui.the_naruno_gui_app


class popup:

    def __init__(
        self,
        title=None,
        text=None,
        image=None,
        height_image=None,
        thirdly_title=None,
        target=None,
        inputs=None,
        type="custom",
    ):
        """
        :param title: Title of the popup
        :param target: Function to be called when the OK button is pressed
        :param content: Content of the popup
        """
        self.title = title
        self.text = text
        self.image = image
        self.height_image = height_image

        self.thirdly_title = thirdly_title
        self.target = target
        self.inputs = inputs
        self.input_results = {}
        self.type = type
        self.dialog = None

        self.create()
        if self.type == "custom":
            self.show()

    def show(self):
        self.dialog.open()

    def dismiss(self, widget=None):
        self.dialog.dismiss()

    def clean(self):

        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                obj.text = ""

    def director(self, widget):
        print("director")

        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                self.input_results[obj.hint_text] = obj.text
        print("Target")
        self.target()
        print("Clean")
        self.clean()
        print("Dismiss")
        self.dismiss()
        print("Done")

    def director_without_input(self, widget):
        print("director")
        self.target()
        self.dismiss()

    def create(self):
        if self.dialog is None:
            if self.type == "custom":
                self.dialog = SweetAlert(
                    title=self.title,
                    type=self.type,
                    auto_dismiss=False,
                    buttons=[
                        MDFlatButton(
                            text="CANCEL",
                            font_size="18sp",
                            on_press=self.dismiss,
                            font_name=os.path.join(
                                naruno.gui.
                                the_naruno_gui_app.
                                the_naruno_gui.FONT_PATH,
                                "Poppins-Bold",
                            ),
                        ),
                        MDFlatButton(
                            text="OK",
                            font_size="18sp",
                            font_name=os.path.join(
                                naruno.gui.
                                the_naruno_gui_app.
                                the_naruno_gui.FONT_PATH,
                                "Poppins-Bold",
                            ),
                            on_press=self.director,
                        ),
                    ],
                )

                for i in self.inputs:
                    content = i[0]
                    is_pass = i[1]
                    self.dialog.content_cls.add_widget(
                        MDTextField(hint_text=content,
                                    mode="fill",
                                    password=is_pass))
            elif self.type != "question":
                the_type = None if self.type == "qr" else self.type
                self.dialog = SweetAlert()
                self.dialog.fire(
                    self.title,
                    self.text,
                    self.thirdly_title,
                    image=self.image,
                    height_image=self.height_image,
                    type=the_type,
                )
            else:
                self.dialog = SweetAlert()
                self.dialog.fire(
                    title=self.title,
                    text=self.text,
                    type=self.type,
                    buttons=[
                        MDFlatButton(
                            text="NO",
                            font_size="18sp",
                            on_press=self.dismiss,
                            font_name=os.path.join(
                                naruno.gui.
                                the_naruno_gui_app.
                                the_naruno_gui.FONT_PATH,
                                "Poppins-Bold",
                            ),
                        ),
                        MDFlatButton(
                            text="YES",
                            font_size="18sp",
                            font_name=os.path.join(
                                naruno.gui.
                                the_naruno_gui_app.
                                the_naruno_gui.FONT_PATH,
                                "Poppins-Bold",
                            ),
                            on_press=self.director_without_input,
                        ),
                    ],
                )
