#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


import os


from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd_extensions.sweetalert import SweetAlert
from kivymd.toast import toast

from kivy.core.clipboard import Clipboard

from node.node_connection import ndstart, ndstop, ndconnect, ndconnectmixdb, ndid

from lib.settings_system import the_settings
from lib.status import Status

from blockchain.block.get_block import GetBlockFromOtherNode
from blockchain.block.create_block import CreateBlock

class NodeScreen(MDScreen):
    pass

# Start Node Server
class start_node_server_Box(MDGridLayout):
    cols = 2
# End

# Add UNL Node
class add_unl_node_Box(MDGridLayout):
    cols = 2
# End

class NodeBox(MDGridLayout):
    cols = 2
    FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"

    # Start Node Server
    start_node_server_dialog = None
    def show_start_node_server_dialog(self):
        if not self.start_node_server_dialog:
            self.start_node_server_dialog = SweetAlert(
                title="Start Node Server",
                type="custom",
                auto_dismiss=False,
                content_cls=start_node_server_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_start_node_server_dialog,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.start_node_server_func,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                ],
            )
        self.start_node_server_dialog.open()


    def get_start_node_server_dialog_text(self):
        text_list = []
        for obj in self.start_node_server_dialog.content_cls.children:
            for sub_obj in obj.children:
                text_list.append(sub_obj.text)
                sub_obj.text = ""

        return text_list  
    def start_node_server_func(self, widget):
        text_list = self.get_start_node_server_dialog_text()
        ip = text_list[1]
        port = text_list[0]

        print(ip)
        print(port)
        
        ndstart(ip, int(port))

        self.start_node_server_dialog.dismiss()
    def dismiss_start_node_server_dialog(self,widget):
        self.get_start_node_server_dialog_text()

        self.start_node_server_dialog.dismiss()


    def start_node_server(self):
        self.show_start_node_server_dialog()
    # End


    def stop_node_server(self):
        ndstop()
    def connect_to_know_node(self):
        ndconnectmixdb()


    # Connect a Node

    connect_a_node_dialog = None
    def show_connect_a_node_dialog(self):
        if not self.connect_a_node_dialog:
            self.connect_a_node_dialog = SweetAlert(
                title="Connect a Node",
                type="custom",
                auto_dismiss=False,
                content_cls=start_node_server_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_connect_a_node_dialog,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.connect_a_node_func,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                ],
            )
        self.connect_a_node_dialog.open()


    def get_connect_a_node_dialog_text(self):
        text_list = []
        for obj in self.connect_a_node_dialog.content_cls.children:
            for sub_obj in obj.children:
                text_list.append(sub_obj.text)
                sub_obj.text = ""

        return text_list  
    def connect_a_node_func(self,widget):
        text_list = self.get_connect_a_node_dialog_text()
        ip = text_list[1]
        port = text_list[0]

        print(ip)
        print(port)
        
        ndconnect(ip, int(port))

        self.connect_a_node_dialog.dismiss()
    def dismiss_connect_a_node_dialog(self,widget):
        self.get_connect_a_node_dialog_text()

        self.connect_a_node_dialog.dismiss()

    def connect_a_node(self):
        self.show_connect_a_node_dialog()
    # End   

    # Add UNL Node

    add_unl_node_dialog = None
    def show_add_unl_node_dialog(self):
        if not self.add_unl_node_dialog:
            self.add_unl_node_dialog = SweetAlert(
                title="Add UNL Node",
                type="custom",
                auto_dismiss=False,
                content_cls=add_unl_node_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_add_unl_node_dialog,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.add_unl_node_func,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                ],
            )
        self.add_unl_node_dialog.open()


    def get_add_unl_node_dialog_text(self):
        text_list = []
        for obj in self.add_unl_node_dialog.content_cls.children:
            for sub_obj in obj.children:
                text_list.append(sub_obj.text)
                sub_obj.text = ""

        return text_list  
    def add_unl_node_func(self,widget):
        text_list = self.get_add_unl_node_dialog_text()
        pubkey = text_list[0]

        print(pubkey)

        from node.unl import save_new_unl_node
        save_new_unl_node(pubkey)        

        self.add_unl_node_dialog.dismiss()
    def dismiss_add_unl_node_dialog(self,widget):
        self.get_add_unl_node_dialog_text()

        self.add_unl_node_dialog.dismiss()

    def add_unl_node(self):
        self.show_add_unl_node_dialog()
    # End
    def get_block(self):
        if the_settings()["test_mode"]:
            CreateBlock()
        else:
            GetBlockFromOtherNode()

    def nd_id(self):
        Clipboard.copy(ndid())
        SweetAlert().fire(
            "The ID has been copied to your clipboard.",
            type='success',
        )

    def status(self):
        toast("Calculating...")
        status = Status()
        if status == "Good":
            SweetAlert().fire(
                "Good",
                type='success',
            )
        elif status == "Not bad":
            SweetAlert().fire(
                "Not bad",
                type='info'
            )
        elif status == "Bad":
            SweetAlert().fire(
                "Not bad",
                type='question'
            )
        elif status == "Very bad":
            SweetAlert().fire(
                "Very bad",
                type='warning'
            )
        elif status == "Not work":
            SweetAlert().fire(
                "Not work",
                type='failure'
            )
