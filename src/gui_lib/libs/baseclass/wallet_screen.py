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

from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDListBottomSheet

from kivy.core.clipboard import Clipboard

from wallet.wallet import Wallet_Create, Wallet_Import, get_saved_wallet

import os

from accounts.get_balance import GetBalance

from blockchain.block.get_block import GetBlock

from lib.settings_system import the_settings, change_wallet

class WalletScreen(MDScreen):
    pass

class Create_Wallet_Box(MDGridLayout):
    cols = 2

class WalletBox(MDGridLayout):
    cols = 2
    text = StringProperty()

    wallet_alert_dialog = None

    FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"

    def reflesh_balance(self):

        self.text = "Balance: "+str(GetBalance(Wallet_Import(-1,0), GetBlock()))

    def show_wallet_alert_dialog(self):
        if not self.wallet_alert_dialog:
            self.wallet_alert_dialog = MDDialog(
                title="Creating a wallet",
                type="custom",
                auto_dismiss=False,
                content_cls=Create_Wallet_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_wallet_alert_dialog,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                        on_press=self.create_the_wallet
                    )
                ],
            )
        self.wallet_alert_dialog.open()

    def callback_for_menu_items(self, *args):
        if not args[0] == the_settings()["wallet"]:
            change_wallet(args[0])
            self.reflesh_balance()
        else:
            change_wallet(args[0])
        Clipboard.copy(Wallet_Import(int(args[0]),3))
        toast("The address has been copied to your clipboard.")

    def show_example_list_bottom_sheet(self):
        bottom_sheet_menu = MDListBottomSheet(radius=25,radius_from="top")
        data = {}
        all_wallets = list(get_saved_wallet())

        current_wallet = the_settings()["wallet"]
        for wallet in all_wallets:
            number = str(all_wallets.index(wallet))
            address = Wallet_Import(all_wallets.index(wallet),3)
            if not current_wallet == number:
                data[number] = address
            else:
                data[number] = address + " - CURRENTLY USED"

        for item in data.items():
            bottom_sheet_menu.add_item(
                item[0] +" : "+ item[1],
                lambda x, y=item[0]: self.callback_for_menu_items(y),

            )
        bottom_sheet_menu.open()

    def dismiss_wallet_alert_dialog(self, widget):
        self.wallet_alert_dialog.dismiss()

    def create_the_wallet(self, widget):
        text_list = []
        for obj in self.wallet_alert_dialog.content_cls.children:
            for sub_obj in obj.children:
                Wallet_Create(sub_obj.text)
                self.dismiss_wallet_alert_dialog(widget)

                sub_obj.text = ""

    def Wallet_Create(self):
        self.show_wallet_alert_dialog()
