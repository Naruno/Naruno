#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from kivy.properties import StringProperty

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen


from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from wallet.wallet import *

import os

class WalletScreen(MDScreen):
    pass


class WalletBox(MDGridLayout):
    cols = 2
    text = StringProperty()

    wallet_alert_dialog = None

    FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"

    def reflesh_balance(self):
        from blockchain.block.block_main import get_block

        self.text = "Balance: "+str(get_block().getBalance(Wallet_Import(0,0)))

    def show_wallet_alert_dialog(self):
        if not self.wallet_alert_dialog:
            self.wallet_alert_dialog = MDDialog(
                title="Wallet is Created",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                        on_press=self.dismiss_wallet_alert_dialog
                    ),
                ],
            )
        self.wallet_alert_dialog.open()

    def dismiss_wallet_alert_dialog(self,widget):
        self.wallet_alert_dialog.dismiss()

    def Wallet_Create(self):
        Wallet_Create()
        self.show_wallet_alert_dialog()
    

