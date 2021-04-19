#!/usr/bin/python3
# -*- coding: utf-8 -*-
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


def clear():
	os.system("clear")


def dprint(text):
    try:
     from lib.settings_system import the_settings
     if the_settings()["debug_mode"]:
         print("DEBUG: "+str(text))
    except Exception as e:
        print(e)	

