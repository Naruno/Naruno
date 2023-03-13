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

from naruno.lib.config_system import get_config


class Naruno_Scene(Scene):
    """
    This scene is explain the Node concept.
    """

    def set_title(self, the_title=""):
        self.the_title = the_title

    def settings(self):
        self.camera.background_color = "#303030"

        self.font = "Poppins"

    def intro_logo(self):
        # Get the logo from grand parent directory
        root_directory = get_config()["main_folder"]

        self.icon = os.path.join(root_directory, "gui_lib", "images", "logo.ico")

        self.image = ImageMobject(self.icon).scale(2)
        self.play(FadeIn(self.image))
        self.wait(1)
        self.play(FadeOut(self.image))

    def intro_text(self):
        """
        Naruno is building on Node.
        """
        text = Text("Naruno", font=self.font, color="#DBFF00")
        self.play(Write(text))
        self.play(text.animate.shift(LEFT * 1))
        text2 = Text(self.the_title, font=self.font).shift(RIGHT * 1)
        self.play(Write(text2))
        self.wait(2)
        self.play(FadeOut(text), FadeOut(text2))

    def creating_nodes(self, node_1="Node 1", node_2="Node 2", node_3="Node 3"):
        """
        In this example, we have four node.
        """
        self.node_1 = Circle(color=WHITE)
        self.node_2 = Circle(color=WHITE).shift(0.5 * UP)
        self.node_3 = Circle(color=WHITE)

        self.node_3.next_to(self.node_2, RIGHT + DOWN, buff=0.5)
        self.node_1.next_to(self.node_2, LEFT + DOWN, buff=0.5)

        self.node_1_text = Text(node_1, font=self.font).next_to(self.node_1, UP)
        self.node_2_text = Text(node_2, font=self.font).next_to(self.node_2, UP)
        self.node_3_text = Text(node_3, font=self.font).next_to(self.node_3, UP)

        self.play(Create(self.node_1), Create(self.node_2), Create(self.node_3))
        self.play(
            Write(self.node_1_text), Write(self.node_2_text), Write(self.node_3_text)
        )
        self.wait()

    def create_node_connections(self):
        """
        And this nodes connects eachone with TCP protocol.
        """
        self.connection_1 = Line(self.node_1.get_center(), self.node_2.get_center())
        self.connection_2 = Line(self.node_2.get_center(), self.node_3.get_center())
        self.connection_3 = Line(self.node_3.get_center(), self.node_1.get_center())

        self.play(
            Create(self.connection_1),
            Create(self.connection_3),
            Create(self.connection_2),
        )

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
            self.security_circle_1_components, UP
        )
        self.security_circle_1 = VGroup(
            self.security_circle_1_components, self.secuirty_circle_1_text
        )
        self.play(
            Create(self.secuirty_circle_1_text),
            self.security_circle_1.animate.set_color("#5EC295").scale(0.5),
        )

    def turn_to_network(self):
        self.play(
            self.circle_1.animate.shift(1.8 * DOWN).shift(2 * RIGHT),
        )

    def create_security_circles(self):
        """
        When a connections are have more than two node, we call security circle.
        """
        self.turn_to_security_circle()

        self.play(self.security_circle_1.animate.shift(2 * UP))

        self.security_circle_2_components = self.security_circle_1_components.copy()
        self.secuirty_circle_2_text = (
            Text("Security Circle 2", font=self.font)
            .next_to(self.security_circle_2_components, UP)
            .set_color("#5EC295")
            .scale(0.5)
        )
        self.security_circle_2 = VGroup(
            self.security_circle_2_components, self.secuirty_circle_2_text
        )
        self.security_circle_3_components = self.security_circle_1_components.copy()
        self.secuirty_circle_3_text = (
            Text("Security Circle 3", font=self.font)
            .next_to(self.security_circle_3_components, UP)
            .set_color("#5EC295")
            .scale(0.5)
        )
        self.security_circle_3 = VGroup(
            self.security_circle_3_components, self.secuirty_circle_3_text
        )
        self.security_circle_4_components = self.security_circle_1_components.copy()
        self.secuirty_circle_4_text = (
            Text("Security Circle 4", font=self.font)
            .next_to(self.security_circle_4_components, UP)
            .set_color("#5EC295")
            .scale(0.5)
        )
        self.security_circle_4 = VGroup(
            self.security_circle_4_components, self.secuirty_circle_4_text
        )

        self.play(
            Create(self.security_circle_2),
            Create(self.security_circle_3),
            Create(self.security_circle_4),
            self.security_circle_1.animate.shift(3 * LEFT),
            self.security_circle_2.animate.shift(3 * RIGHT),
            self.security_circle_3.animate.shift(3 * LEFT + 3.5 * DOWN),
            self.security_circle_4.animate.shift(3 * RIGHT + 3.5 * DOWN),
        )

        self.wait(2)

        self.circle_1 = Circle(color="#5EC295").scale(1.5).shift(2 * UP).shift(3 * LEFT)
        self.circle_2 = (
            Circle(color="#5EC295").scale(1.5).shift(2 * UP).shift(3 * RIGHT)
        )
        self.circle_3 = (
            Circle(color="#5EC295")
            .scale(1.5)
            .shift(2 * UP)
            .shift(3 * LEFT + 3.5 * DOWN)
        )
        self.circle_4 = (
            Circle(color="#5EC295")
            .scale(1.5)
            .shift(2 * UP)
            .shift(3 * RIGHT + 3.5 * DOWN)
        )
        self.play(
            ReplacementTransform(self.security_circle_1, self.circle_1),
            ReplacementTransform(self.security_circle_2, self.circle_2),
            ReplacementTransform(self.security_circle_3, self.circle_3),
            ReplacementTransform(self.security_circle_4, self.circle_4),
        )

        self.wait(2)

    def creates_network(self):
        """
        And the security circles creates network.
        """
        self.play(
            self.circle_1.animate.shift(1.8 * DOWN).shift(2 * RIGHT),
            self.circle_2.animate.shift(1.8 * DOWN).shift(2 * LEFT),
            self.circle_3.animate.shift(1.8 * DOWN).shift(2 * RIGHT + 2.5 * UP),
            self.circle_4.animate.shift(1.8 * DOWN).shift(2 * LEFT + 2.5 * UP),
        )

        # intersections of the circles
        self.i_all = Intersection(
            self.circle_1, self.circle_2, self.circle_3, self.circle_4
        )
        self.i_12 = Intersection(self.circle_1, self.circle_2)
        self.i_13 = Intersection(self.circle_1, self.circle_3)
        self.i_14 = Intersection(self.circle_1, self.circle_4)
        self.i_23 = Intersection(self.circle_2, self.circle_3)
        self.i_24 = Intersection(self.circle_2, self.circle_4)
        self.i_34 = Intersection(self.circle_3, self.circle_4)
        # fill the intersections
        self.play(
            self.i_all.animate.set_fill(color="#5EC295", opacity=0.5),
            self.i_12.animate.set_fill(color="#5EC295", opacity=0.5),
            self.i_13.animate.set_fill(color="#5EC295", opacity=0.5),
            self.i_14.animate.set_fill(color="#5EC295", opacity=0.5),
            self.i_23.animate.set_fill(color="#5EC295", opacity=0.5),
            self.i_24.animate.set_fill(color="#5EC295", opacity=0.5),
            self.i_34.animate.set_fill(color="#5EC295", opacity=0.5),
        )
        self.wait(1)
        self.play(
            self.i_all.animate.set_fill(color="#5EC295", opacity=0),
            self.i_12.animate.set_fill(color="#5EC295", opacity=0),
            self.i_13.animate.set_fill(color="#5EC295", opacity=0),
            self.i_14.animate.set_fill(color="#5EC295", opacity=0),
            self.i_23.animate.set_fill(color="#5EC295", opacity=0),
            self.i_24.animate.set_fill(color="#5EC295", opacity=0),
            self.i_34.animate.set_fill(color="#5EC295", opacity=0),
        )

    def data_running_through_the_intersections_and_circles(self):
        """
        And all of signed and safe datas running arround of intersections and inside of circles.
        """
        self.dot_i_all = Dot(color="#5EC295").move_to(self.i_all.get_right()).scale(1.5)
        self.dot_i_12 = Dot(color="#5EC295").move_to(self.i_12.get_right()).scale(1.5)
        self.dot_i_13 = Dot(color="#5EC295").move_to(self.i_13.get_right()).scale(1.5)
        self.dot_i_14 = Dot(color="#5EC295").move_to(self.i_14.get_right()).scale(1.5)
        self.dot_i_23 = Dot(color="#5EC295").move_to(self.i_23.get_right()).scale(1.5)
        self.dot_i_24 = Dot(color="#5EC295").move_to(self.i_24.get_right()).scale(1.5)
        self.dot_i_34 = Dot(color="#5EC295").move_to(self.i_34.get_right()).scale(1.5)

        self.dot_circle_1 = (
            Dot(color="#5EC295").move_to(self.circle_1.get_right()).scale(1.5)
        )
        self.dot_circle_2 = (
            Dot(color="#5EC295").move_to(self.circle_2.get_right()).scale(1.5)
        )
        self.dot_circle_3 = (
            Dot(color="#5EC295").move_to(self.circle_3.get_right()).scale(1.5)
        )
        self.dot_circle_4 = (
            Dot(color="#5EC295").move_to(self.circle_4.get_right()).scale(1.5)
        )

        self.play(
            MoveAlongPath(self.dot_i_all, self.i_all),
            MoveAlongPath(self.dot_i_12, self.i_12),
            MoveAlongPath(self.dot_i_13, self.i_13),
            MoveAlongPath(self.dot_i_14, self.i_14),
            MoveAlongPath(self.dot_i_23, self.i_23),
            MoveAlongPath(self.dot_i_24, self.i_24),
            MoveAlongPath(self.dot_i_34, self.i_34),
            MoveAlongPath(self.dot_circle_1, self.circle_1),
            MoveAlongPath(self.dot_circle_2, self.circle_2),
            MoveAlongPath(self.dot_circle_3, self.circle_3),
            MoveAlongPath(self.dot_circle_4, self.circle_4),
            run_time=2,
        )
        self.wait(2)

    def clear_scren(self):
        self.play(
            FadeOut(self.circle_1),
            FadeOut(self.circle_2),
            FadeOut(self.circle_3),
            FadeOut(self.circle_4),
            FadeOut(self.dot_i_all),
            FadeOut(self.dot_i_12),
            FadeOut(self.dot_i_13),
            FadeOut(self.dot_i_14),
            FadeOut(self.dot_i_23),
            FadeOut(self.dot_i_24),
            FadeOut(self.dot_i_34),
            FadeOut(self.dot_circle_1),
            FadeOut(self.dot_circle_2),
            FadeOut(self.dot_circle_3),
            FadeOut(self.dot_circle_4),
            FadeOut(self.i_all),
            FadeOut(self.i_12),
            FadeOut(self.i_13),
            FadeOut(self.i_14),
            FadeOut(self.i_23),
            FadeOut(self.i_24),
            FadeOut(self.i_34),
        )


if __name__ == "__main__":
    Node().render()
