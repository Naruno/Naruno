#!/usr/bin/python3
# -*- coding: utf-8 -*-
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivymd.uix.screen import MDScreen


class NarunoWelcomeScreen(MDScreen):
    pb = ProgressBar()

    def __init__(self, *args, **kwargs):
        super(NarunoWelcomeScreen, self).__init__(*args, **kwargs)
        self.update_bar_trigger = Clock.schedule_interval(
            self.update_bar, 0.01)

    def update_bar(self, dt):
        if self.ids.pb.value < 100:
            self.ids.pb.value += 1
        else:
            self.update_bar_trigger.cancel()
            self.manager.current = "naruno root screen"
