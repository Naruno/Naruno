#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kivy.properties import ColorProperty
from kivy.properties import StringProperty
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

import decentra_network.gui.the_decentra_network_gui_app

from decentra_network.gui.popup import popup


class DecentraRootScreen(MDScreen):
    def close_app(self, widget=None):
        self.close_app_dialog = popup(
            title=decentra_network.gui.the_decentra_network_gui_app.the_decentra_network_gui.title, 
            text="Are you sure you want to close ?", 
            target=decentra_network.gui.the_decentra_network_gui_app.the_decentra_network_gui.stop,
            type="question"
            )


class DecentraListItem(ThemableBehavior, RectangularRippleBehavior,
                       MDBoxLayout):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    bar_color = ColorProperty((1, 0, 0, 1))


class DecentraSeeAllButton(RectangularRippleBehavior, MDBoxLayout):
    pass
