#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

import naruno.gui.the_naruno_gui_app
from naruno.blockchain.block.create_block import CreateBlock
from naruno.blockchain.block.save_block import SaveBlock
from naruno.consensus.consensus_main import consensus_trigger
from naruno.gui.popup import popup
from naruno.lib.perpetualtimer import perpetualTimer
from naruno.lib.qr import qr
from naruno.lib.settings_system import the_settings
from naruno.lib.status import Status
from naruno.node.server.server import server


class NodeScreen(MDScreen):
    pass



class NodeBox(MDGridLayout):
    cols = 2

    def start_node_server_func(self):
        server(
            self.start_node_server_dialog.input_results["IP"],
            int(self.start_node_server_dialog.input_results["PORT"]),
        )

    def show_start_node_server_dialog(self):
        self.start_node_server_dialog = popup(
            title="Start Node Server",
            target=self.start_node_server_func,
            inputs=[
                ["IP", False],
                ["PORT", False],
            ],
        )

    def check_node_server(self):
        if server.Server is None:
            popup(title="Please start the node server", type="failure")
            return False
        return True

    def stop_node_server(self):
        if not self.check_node_server():
            return False
        server.Server.stop()

    def connect_to_know_node(self):
        server.connectionfrommixdb()

    def connect_a_node_func(self):

        if not self.check_node_server():
            return False
        server.Server.connect(
            self.connect_a_node_dialog.input_results["IP"],
            int(self.connect_a_node_dialog.input_results["PORT"]),
        )

    def show_connect_a_node_dialog(self):
        self.connect_a_node_dialog = popup(
            title="Connect a Node",
            target=self.connect_a_node_func,
            inputs=[
                ["IP", False],
                ["PORT", False],
            ],
        )

    def add_unl_node_func(self):

        from naruno.node.unl import Unl

        Unl.save_new_unl_node(
            self.add_unl_node_dialog.input_results["PublicKey"])

    def show_add_unl_node_dialog(self):
        self.add_unl_node_dialog = popup(
            title="Add UNL Node",
            target=self.add_unl_node_func,
            inputs=[
                ["PublicKey", False],
            ],
        )

    def get_block(self):
        if not self.check_node_server():
            return False
        if the_settings()["test_mode"]:
            the_block = CreateBlock()
            SaveBlock(the_block)
            server.Server.send_block_to_other_nodes()
            perpetualTimer(the_block.consensus_timer, consensus_trigger)
        else:
            server.Server.send_me_full_block()

    def nd_id(self):
        Clipboard.copy(server.id)
        popup(title="The ID has been copied to your clipboard.",
              type="success")

    def nd_id_qr(self):
        location_of_qr = qr(server.id)
        popup(text=server.id,
              image=location_of_qr,
              height_image="450px",
              type="qr")

    def status(self):
        toast("Calculating...")
        status = Status()
        if status == "Good":
            popup(title="Good", type="success")

        elif status == "Not bad":
            popup(title="Not bad", type="info")
        elif status == "Bad":
            popup(title="Bad", type="warning")
        elif status == "Very bad":
            popup(title="Very bad", type="warning")
        elif status == "Not work":
            popup(title="Not work", type="failure")
