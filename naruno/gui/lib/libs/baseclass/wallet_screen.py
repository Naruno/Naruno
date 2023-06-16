#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd_extensions.sweetalert import SweetAlert

import naruno.gui.the_naruno_gui_app
from naruno.accounts.get_balance import GetBalance
from naruno.blockchain.block.get_block import GetBlock
from naruno.gui.popup import popup
from naruno.lib.qr import qr
from naruno.lib.settings_system import change_wallet
from naruno.lib.settings_system import the_settings
from naruno.wallet.get_saved_wallet import get_saved_wallet
from naruno.wallet.wallet_create import wallet_create
from naruno.wallet.wallet_delete import wallet_delete
from naruno.wallet.wallet_import import wallet_import


class WalletScreen(MDScreen):
    pass


class WalletBox(MDGridLayout):
    cols = 2
    text = StringProperty()

    def reflesh_balance(self):

        self.text = f"Balance: {str(GetBalance(wallet_import(-1, 0)))}"

    def create_the_wallet(self):
        wallet_create(self.wallet_alert_dialog.input_results["Password"])

    def show_wallet_alert_dialog(self):
        self.wallet_alert_dialog = popup(
            title="Creating a wallet",
            target=self.create_the_wallet,
            inputs=[["Password", True]],
        )

    def callback_for_menu_items(self, *args):
        if args[0] != the_settings()["wallet"]:
            change_wallet(int(args[0]))
            self.reflesh_balance()

    def show_example_list_bottom_sheet(self):
        bottom_sheet_menu = MDListBottomSheet(radius=25, radius_from="top")
        data = {}
        all_wallets = list(get_saved_wallet())

        current_wallet = the_settings()["wallet"]
        for wallet in all_wallets:
            number = all_wallets.index(wallet)
            address = wallet_import(all_wallets.index(wallet), 3)
            if current_wallet != number:
                data[number] = address
            else:
                data[number] = f"{address} - CURRENTLY USED"

        for item in data.items():
            bottom_sheet_menu.add_item(
                f"{str(item[0])} : {item[1]}",
                lambda x, y=item[0]: self.callback_for_menu_items(y),
            )

        bottom_sheet_menu.open()

    def delete_the_wallet(self):
        saved_wallets = get_saved_wallet()
        selected_wallet_pubkey = wallet_import(int(the_settings()["wallet"]),
                                               0)
        for each_wallet in saved_wallets:
            if selected_wallet_pubkey == saved_wallets[each_wallet][
                    "publickey"]:
                change_wallet(0)
                wallet_delete(each_wallet)
                self.reflesh_balance()

    def show_delete_wallet_alert_dialog(self):
        if the_settings()["wallet"] != 0:
            self.deletewallet_alert_dialog = popup(
                title="Deleting a wallet",
                target=self.delete_the_wallet,
                type="question",
            )
        else:
            popup(title="First wallet cannot be deleted.", type="failure")

    def wallet_qr(self):
        address = wallet_import(-1, 3)
        location_of_qr = qr(address)
        popup(text=address,
              image=location_of_qr,
              height_image="400px",
              type="qr")

    def wallet_copy(self):
        Clipboard.copy(wallet_import(-1, 3))
        popup(title="The address has been copied to your clipboard.",
              type="success")
