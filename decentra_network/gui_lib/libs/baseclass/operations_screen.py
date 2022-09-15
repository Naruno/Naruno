#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from hashlib import sha256

from kivy.core.clipboard import Clipboard
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.button import MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd_extensions.sweetalert import SweetAlert

from decentra_network.blockchain.block.get_block import GetBlock
from decentra_network.blockchain.block.save_block import SaveBlock
from decentra_network.config import MY_TRANSACTION_EXPORT_PATH
from decentra_network.lib.export import export_the_transactions
from decentra_network.lib.settings_system import the_settings
from decentra_network.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from decentra_network.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from decentra_network.transactions.send import send
from decentra_network.wallet.ellipticcurve.wallet_import import wallet_import


class OperationScreen(MDScreen):
    pass


class Send_Coin_Box(MDGridLayout):
    cols = 2


class OperationBox(MDGridLayout):
    cols = 2
    send_coin_dialog = None
    export_transaction_csv_dialog = None
    FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"

    def show_send_coin_dialog(self):
        if not self.send_coin_dialog:
            self.send_coin_dialog = SweetAlert(
                title="Send Coin",
                type="custom",
                auto_dismiss=False,
                content_cls=Send_Coin_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_send_coin_dialog,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.sent_the_coins,
                        font_size="18sp",
                        font_name=f"{self.FONT_PATH}RobotoCondensed-Bold",
                    ),
                ],
            )

        self.send_coin_dialog.open()

    def get_send_coin_dialog_text(self):
        text_list = []
        for obj in self.send_coin_dialog.content_cls.children:
            for sub_obj in obj.children:
                text_list.append(sub_obj.text)

                sub_obj.text = ""

        return text_list

    def sent_the_coins(self, widget):

        text_list = self.get_send_coin_dialog_text()
        receiver_adress = text_list[2]
        amount = text_list[1]

        if float(amount) >= GetBlock().minumum_transfer_amount:
            if (wallet_import(int(the_settings()["wallet"]), 2) == sha256(
                    text_list[0].encode("utf-8")).hexdigest()):
                block = GetBlock()
                send_tx = send(text_list[0],
                               receiver_adress,
                               amount=float(amount),
                               block=block)
                if send_tx != False:
                    from decentra_network.node.server.server import server

                    SavetoMyTransaction(send_tx, sended=True)
                    server.send_transaction(send_tx)
                    SaveBlock(block)
            else:
                SweetAlert().fire(
                    "Password is not correct",
                    type="failure",
                )
            del text_list

        self.send_coin_dialog.dismiss()

    def dismiss_send_coin_dialog(self, widget):
        self.get_send_coin_dialog_text()

        self.send_coin_dialog.dismiss()

    def send_coin(self):
        self.show_send_coin_dialog()

    def export_transaction_csv(self):
        if export_the_transactions():
            Clipboard.copy(MY_TRANSACTION_EXPORT_PATH)
            SweetAlert().fire(
                f"CSV file created in {MY_TRANSACTION_EXPORT_PATH} directory, The directory has been copied to your clipboard.",
                type="success",
            )
        else:
            SweetAlert().fire(
                "You have not a transaction",
                type="failure",
            )

    def callback_for_transaction_history_items(self, widget):
        pass

    def transaction_history(self):
        transactions = GetMyTransaction()
        if len(transactions) != 0:
            bottom_sheet_menu = MDListBottomSheet(radius=25, radius_from="top")
            data = {
                tx[0]:
                f"{tx[0].toUser} | {str(tx[0].amount)} | {str(tx[0].transaction_fee)} | {str(tx[1])}"
                for tx in transactions
            }

            for item in data.items():
                bottom_sheet_menu.add_item(
                    item[1],
                    lambda x, y=item[0]: self.
                    callback_for_transaction_history_items(y),
                )
            bottom_sheet_menu.open()
        else:
            SweetAlert().fire(
                "You have not a transaction",
                type="failure",
            )
