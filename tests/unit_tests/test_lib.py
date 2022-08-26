#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
import unittest
from unittest import mock

from decentra_network.lib.clean_up import CleanUp_tests
from decentra_network.lib.mix.mixlib import (banner_maker, ended_text_centered,
                                             menu_maker, menu_seperator,
                                             menu_space, menu_title,
                                             printcentertext, question_maker,
                                             quit_menu_maker,
                                             starting_text_centered)


class Test_Lib(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        CleanUp_tests()

    def test_starting_text_centered(self):
        self.assertEqual(starting_text_centered(), "\nSTARTING\n")

    def test_ended_text_centered(self):
        self.assertEqual(ended_text_centered(), "\nENDED\n")

    def test_printcentertext(self):
        self.assertEqual(printcentertext("text"), "\ntext\n")

    def test_banner_maker(self):
        sc_name = "sc_name"
        description = "sc_version"
        author = "sc_description"

        self.assertEqual(
            banner_maker(sc_name, description, author),
            (((((f"""Script Name    : {sc_name}""" + """\n""" +
                 """Description    : """) + description) + """\n""") +
              """Author         : """) + author) + """\n""",
        )

    def test_menu_maker(self):
        menu_number = 1
        menu_text = "menu_text"
        self.assertEqual(
            menu_maker(menu_number, menu_text),
            f"{str(menu_number)}) {menu_text}" + "\n",
        )

    def test_quit_menu_maker_main(self):
        self.assertEqual(quit_menu_maker("main"), "\n0) Quit \n")

    def test_quit_menu_maker_sub(self):
        self.assertEqual(quit_menu_maker("sub"), "\n0) Quit sub menu \n")

    def test_quit_menu_maker_other(self):
        self.assertEqual(quit_menu_maker("maina"), "\n0) Quit \n")

    def test_menu_space(self):
        self.assertEqual(menu_space(), "\n")

    def test_menu_seperator(self):
        self.assertEqual(menu_seperator(), "\n*** \n\n")

    def test_menu_title(self):
        self.assertEqual(menu_title("title"), "\n*** title *** \n\n")

    def test_question_maker_custom_Text(self):
        question_text = "question_text"
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(question_text), 1)

    def test_question_maker_main(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="main"), 1)

    def test_question_maker_sub(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="sub"), 1)

    def test_question_maker_anykeytocontinue(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="anykeytocontinue"), 1)

    def test_question_maker_other(self):
        with mock.patch("builtins.input", return_value=1):
            self.assertEqual(question_maker(mode="maina"), 1)


unittest.main(exit=False)
