#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

import decentra_network.gui.the_decentra_network_gui_app
from decentra_network.blockchain.block.create_block import CreateBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.consensus.consensus_main import consensus_trigger
from decentra_network.gui.popup import popup
from decentra_network.lib.perpetualtimer import perpetualTimer
from decentra_network.lib.qr import qr
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

        from decentra_network.node.unl import Unl

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
