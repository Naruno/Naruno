#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

from decentra_network.accounts.get_balance import GetBalance
from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.lib.qr import qr
from decentra_network.lib.settings_system import change_wallet
from decentra_network.lib.settings_system import the_settings
from decentra_network.wallet.ellipticcurve.get_saved_wallet import \
    get_saved_wallet
from decentra_network.wallet.ellipticcurve.wallet_create import wallet_create
from decentra_network.wallet.ellipticcurve.wallet_delete import wallet_delete
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import


class WalletScreen(MDScreen):
    pass


class Create_Wallet_Box(MDGridLayout):
    cols = 2


class Delete_Wallet_Box(MDGridLayout):
    cols = 2


class WalletBox(MDGridLayout):
    cols = 2
    text = StringProperty()

    wallet_alert_dialog = None
    delete_wallet_alert_dialog = None

    FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"

    def reflesh_balance(self):

        self.text = f"Balance: {str(GetBalance(wallet_import(-1, 0)))}"

    def show_wallet_alert_dialog(self):
        if not self.wallet_alert_dialog:
            self.wallet_alert_dialog = SweetAlert(
                title="Creating a wallet",
                type="custom",
                auto_dismiss=False,
                content_cls=Create_Wallet_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_wallet_alert_dialog,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}Poppins-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}Poppins-Bold",
                        on_press=self.create_the_wallet,
                    ),
                ],
            )

        self.wallet_alert_dialog.open()

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

    def dismiss_wallet_alert_dialog(self, widget):
        self.wallet_alert_dialog.dismiss()

    def create_the_wallet(self, widget):
        for obj in self.wallet_alert_dialog.content_cls.children:
            for sub_obj in obj.children:
                wallet_create(sub_obj.text)
                self.dismiss_wallet_alert_dialog(widget)

                sub_obj.text = ""

    def Wallet_Create(self):
        self.show_wallet_alert_dialog()

    def dismiss_delete_wallet_alert_dialog(self, widget):
        self.delete_wallet_alert_dialog.dismiss()

    def show_delete_wallet_alert_dialog(self):
        if not self.delete_wallet_alert_dialog:
            self.delete_wallet_alert_dialog = SweetAlert(
                title="Deleting a wallet",
                type="custom",
                auto_dismiss=False,
                content_cls=Delete_Wallet_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_delete_wallet_alert_dialog,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}Poppins-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}Poppins-Bold",
                        on_press=self.delete_the_wallet,
                    ),
                ],
            )

        self.delete_wallet_alert_dialog.open()

    def Wallet_Delete(self):
        if the_settings()["wallet"] != 0:
            self.show_delete_wallet_alert_dialog()
        else:
            SweetAlert().fire(
                "First wallet cannot be deleted.",
                type="failure",
            )

    def delete_the_wallet(self, widget):
        saved_wallets = get_saved_wallet()
        selected_wallet_pubkey = wallet_import(int(the_settings()["wallet"]),
                                               0)
        for each_wallet in saved_wallets:
            if selected_wallet_pubkey == saved_wallets[each_wallet][
                    "publickey"]:
                change_wallet(0)
                wallet_delete(each_wallet)
                self.reflesh_balance()
                self.dismiss_delete_wallet_alert_dialog(widget)

    def wallet_qr(self):
        address = wallet_import(-1, 3)
        location_of_qr = qr(address)
        SweetAlert().fire(text=address,
                          image=location_of_qr,
                          height_image="400px")

    def wallet_copy(self):
        Clipboard.copy(wallet_import(-1, 3))
        SweetAlert().fire(
            "The address has been copied to your clipboard.",
            type="success",
        )
