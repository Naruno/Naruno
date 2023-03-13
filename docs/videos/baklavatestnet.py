#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
from unicodedata import name

from manim import *

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from docs.videos.main import Naruno_Scene
from naruno.lib.config_system import get_config


class BaklavaTestNet_Scene(Naruno_Scene):

    def construct(self):
        self.set_title("Baklava TestNet")
        self.settings()
        self.intro_logo()
        self.intro_text(position=2)

        self.creating_nodes()

        self.wait(2)
        self.create_node_connections()
        self.wait(3)
        self.turn_to_security_circle(circle_1="Baklava TestNet")
        self.wait(4)
        self.turn_to_network()
        self.wait(2)

        self.create_users_arround_circle()
        self.wait(3)
        self.user_datas()
        self.wait(5)

        self.user_datas_changing()
        self.wait(5)

        self.clear_baklava_scren()
        self.intro_logo()




    def turn_to_security_circle(self, circle_1="Security Circle 1"):
        self.play(
            FadeOut(self.node_1_text),
            FadeOut(self.node_2_text),
            FadeOut(self.node_3_text),
        )
        self.security_circle_1_components = VGroup(
            self.node_1,
            self.node_2,
            self.node_3,
            self.connection_1,
            self.connection_2,
            self.connection_3,
        )
        self.secuirty_circle_1_text = Text(circle_1, font=self.font).next_to(
            self.security_circle_1_components, UP)
        self.security_circle_1 = VGroup(self.security_circle_1_components,
                                        self.secuirty_circle_1_text)
        self.play(
            Create(self.secuirty_circle_1_text),
            self.security_circle_1.animate.set_color("#5EC295").scale(0.5),
        )

    def turn_to_network(self):
        self.circle_1 = Circle(color="#5EC295").scale(1.5)
        #self.play(self.circle_1.animate.shift(1.8 * DOWN).shift(2 * RIGHT), )

        self.play(ReplacementTransform(self.security_circle_1,
                                       self.circle_1), )


    def create_users_arround_circle(self):
        # Create users
        self.user_1 = Circle(color="#5EC295").scale(0.2)
        self.user_2 = Circle(color="#5EC295").scale(0.2)
        self.user_3 = Circle(color="#5EC295").scale(0.2)
        self.user_4 = Circle(color="#5EC295").scale(0.2)
        self.user_5 = Circle(color="#5EC295").scale(0.2)

        # Create user texts
        self.user_1_text = Text("User 1", font=self.font).next_to(
            self.user_1, 0.3 * DOWN).scale(0.4)
        self.user_2_text = Text("User 2", font=self.font).next_to(
            self.user_2, 0.3 * DOWN).scale(0.4)
        self.user_3_text = Text("User 3", font=self.font).next_to(
            self.user_3, 0.3 * DOWN).scale(0.4)
        self.user_4_text = Text("User 4", font=self.font).next_to(
            self.user_4, 0.3 * DOWN).scale(0.4)


        # Create user groups
        self.user_1_group = VGroup(self.user_1, self.user_1_text).shift(2.5 * UP)
        self.user_2_group = VGroup(self.user_2, self.user_2_text).shift(2.5 * DOWN)
        self.user_3_group = VGroup(self.user_3, self.user_3_text).shift(2.5 * LEFT)
        self.user_4_group = VGroup(self.user_4, self.user_4_text).shift(2.5 * RIGHT)


        # Create the users around the top bottom and left right of circle
        # Move the users around the circle
        self.play(
            Create(self.user_1_group),
            Create(self.user_2_group),
            Create(self.user_3_group),
            Create(self.user_4_group),
        )



    def user_datas(self):
        """
        And all of signed and safe datas running arround of intersections and inside of circles.
        """

        # Create four dots on circle lines and change their location with MoveAlongPath to other users
        self.dot_1 = Dot(color="#FFFFFF").scale(1.5)
        self.dot_2 = Dot(color="#FFFFFF").scale(1.5)
        self.dot_3 = Dot(color="#FFFFFF").scale(1.5)
        self.dot_4 = Dot(color="#FFFFFF").scale(1.5)

        #Set the dots on the circle top bottom and left right
        self.dot_1.move_to(self.circle_1.get_top())
        self.dot_2.move_to(self.circle_1.get_bottom())
        self.dot_3.move_to(self.circle_1.get_left())
        self.dot_4.move_to(self.circle_1.get_right())

        # Creates the dots

        self.play(
            Create(self.dot_1),
            Create(self.dot_2),
            Create(self.dot_3),
            Create(self.dot_4),
        )

    def user_datas_changing(self):
        # Move the dots to the users
        self.play(
            self.dot_1.animate.move_to(self.user_3_group),
            self.dot_2.animate.move_to(self.user_1_group),
            self.dot_3.animate.move_to(self.user_4_group),
            self.dot_4.animate.move_to(self.user_2_group),
        )        
        

    def clear_baklava_scren(self):
        self.play(
            FadeOut(self.circle_1), 
            FadeOut(self.user_1_group),
            FadeOut(self.user_2_group),
            FadeOut(self.user_3_group),
            FadeOut(self.user_4_group),
            FadeOut(self.dot_1),
            FadeOut(self.dot_2),
            FadeOut(self.dot_3),
            FadeOut(self.dot_4),

        )

if __name__ == "__main__":
    Baklava_TestNet_Scene().render()
