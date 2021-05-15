#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2021 Decentra Network Developers
Copyright (c) 2021 Onur Atakan ULUSOY

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os


def starting_text_centered():
	print(" ")
	print(" STARTING \n")


def ended_text_centered():
	print(" ")
	print(" ENDED \n")


def printcentertext(text):
	print(" ")
	print(text)
	print(" ")


def banner_maker(sc_name, description, author):
	return("""Script Name    : """+sc_name+"""\n"""+"""Description    : """+description+"""\n"""+"""Author         : """+author+"""\n""")


def question_maker(question_text=None, mode=None):
	
	if question_text is None:
		if mode == "main":
			question_text = "Please enter main option: "
		elif mode == "sub":
			question_text = "Please enter sub option: "
		elif mode == "anykeytocontinue":
			question_text = "Press any key to continue..."
		else:
			raise ValueError("the mode variable contains an unplanned value")
	
	return(input(question_text))


def menu_maker(menu_number, menu_text):
	return(str(menu_number)+") "+menu_text+"\n")
	

def quit_menu_maker(mode):
	if mode == "main":
		quit_menu_maker_result = "\n0) Quit \n"
	elif mode == "sub":
		quit_menu_maker_result = "\n0) Quit sub menu \n"
	else:
		raise ValueError("the mode variable contains the unplanned value")
	return(quit_menu_maker_result)


def menu_space():
	return("\n")


def menu_seperator():
	return("\n"+"*** \n"+"\n")


def menu_title(menu_title_text):
	return("\n"+"*** "+menu_title_text+" ***"+" \n"+"\n")


def dprint(text):
    try:
     from lib.settings_system import the_settings
     if the_settings()["debug_mode"]:
         print("DEBUG: "+str(text))
    except Exception as e:
        print(e)	

