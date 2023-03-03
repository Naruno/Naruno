#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kivy.properties import ColorProperty
from kivy.properties import StringProperty
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

import naruno.gui.the_naruno_gui_app
from naruno.gui.popup import popup


class NarunoRootScreen(MDScreen):

    def close_app(self, widget=None):
        self.close_app_dialog = popup(
            text="Are you sure you want to close ?",
            target=naruno.gui.the_naruno_gui_app.
            the_naruno_gui.stop,
            type="question",
        )


class NarunoListItem(ThemableBehavior, RectangularRippleBehavior,
                       MDBoxLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    bar_color = ColorProperty((1, 0, 0, 1))


class NarunoSeeAllButton(RectangularRippleBehavior, MDBoxLayout):
    pass
