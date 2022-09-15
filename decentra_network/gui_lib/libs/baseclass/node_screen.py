#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

from decentra_network.blockchain.block.create_block import CreateBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.consensus.consensus_main import consensus_trigger
from decentra_network.lib.perpetualtimer import perpetualTimer
from decentra_network.lib.settings_system import the_settings
from decentra_network.lib.status import Status
from decentra_network.node.server.server import server


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
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.start_node_server_func,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
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

        server(ip, int(port))

        self.start_node_server_dialog.dismiss()

    def dismiss_start_node_server_dialog(self, widget):
        self.get_start_node_server_dialog_text()

        self.start_node_server_dialog.dismiss()

    def start_node_server(self):
        self.show_start_node_server_dialog()

    # End

    def stop_node_server(self):
        server.Server.stop()

    def connect_to_know_node(self):
        server.connectionfrommixdb()

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
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.connect_a_node_func,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
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

    def connect_a_node_func(self, widget):
        text_list = self.get_connect_a_node_dialog_text()
        ip = text_list[1]
        port = text_list[0]

        print(ip)
        print(port)

        server.Server.connect(ip, int(port))

        self.connect_a_node_dialog.dismiss()

    def dismiss_connect_a_node_dialog(self, widget):
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
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.add_unl_node_func,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
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

    def add_unl_node_func(self, widget):
        text_list = self.get_add_unl_node_dialog_text()
        pubkey = text_list[0]

        print(pubkey)

        from decentra_network.node.unl import Unl

        Unl.save_new_unl_node(pubkey)

        self.add_unl_node_dialog.dismiss()

    def dismiss_add_unl_node_dialog(self, widget):
        self.get_add_unl_node_dialog_text()

        self.add_unl_node_dialog.dismiss()

    def add_unl_node(self):
        self.show_add_unl_node_dialog()

    def get_block(self):
        if the_settings()["test_mode"]:
            the_block = CreateBlock()
            SaveBlock(the_block)
            server.Server.send_block_to_other_nodes()
            perpetualTimer(the_block.consensus_timer, consensus_trigger)
        else:
            server.Server.send_me_full_block()

    def nd_id(self):
        Clipboard.copy(server.id)
        SweetAlert().fire(
            "The ID has been copied to your clipboard.",
            type="success",
        )

    def status(self):
        toast("Calculating...")
        status = Status()
        if status == "Good":
            SweetAlert().fire(
                "Good",
                type="success",
            )
        elif status == "Not bad":
            SweetAlert().fire("Not bad", type="info")
        elif status == "Bad":
            SweetAlert().fire("Not bad", type="question")
        elif status == "Very bad":
            SweetAlert().fire("Very bad", type="warning")
        elif status == "Not work":
            SweetAlert().fire("Not work", type="failure")
