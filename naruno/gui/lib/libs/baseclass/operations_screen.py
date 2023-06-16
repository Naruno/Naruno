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

import naruno.gui.the_naruno_gui_app
from naruno.blockchain.block.get_block import GetBlock
from naruno.blockchain.block.save_block import SaveBlock
from naruno.config import MY_TRANSACTION_EXPORT_PATH
from naruno.gui.popup import popup
from naruno.lib.export import export_the_transactions
from naruno.lib.settings_system import the_settings
from naruno.lib.sign import sign
from naruno.lib.verify import verify
from naruno.transactions.my_transactions.get_my_transaction import \
    GetMyTransaction
from naruno.transactions.my_transactions.save_to_my_transaction import \
    SavetoMyTransaction
from naruno.transactions.send import send
from naruno.wallet.wallet_import import wallet_import


class OperationScreen(MDScreen):
    pass


class OperationBox(MDGridLayout):
    cols = 2

    def sent_the_coins(self):
        the_block = GetBlock()

        if (float(self.send_coin_dialog.input_results["Amount"]) >=
                the_block.minumum_transfer_amount):
            if (wallet_import(int(the_settings()["wallet"]), 2) == sha256(
                    self.send_coin_dialog.input_results["Password"].encode(
                        "utf-8")).hexdigest()):
                block = the_block
                send_tx = send(
                    self.send_coin_dialog.input_results["Password"],
                    self.send_coin_dialog.input_results["Receiver"],
                    amount=float(
                        self.send_coin_dialog.input_results["Amount"]),
                    data=str(self.send_coin_dialog.input_results["Data"]),
                    block=block,
                )
                if send_tx != False:

                    from naruno.node.server.server import server

                    if server.Server is None:
                        popup(title="Please start the node server",
                              type="failure")
                        return False

                    SavetoMyTransaction(send_tx, sended=True)
                    server.send_transaction(send_tx)
                    SaveBlock(block)
            else:
                popup(title="Password is not correct", type="failure")

    def show_send_coin_dialog(self):
        self.send_coin_dialog = popup(
            title="Send Coin",
            target=self.sent_the_coins,
            inputs=[
                ["Receiver", False],
                ["Amount", False],
                ["Data", False],
                ["Password", True],
            ],
        )

    def sign_the_data(self):
        path = sign(
            self.sign_dialog.input_results["Data"],
            self.sign_dialog.input_results["Password"],
        )
        if path == "None":
            popup(title="Password is not correct", type="failure")
        else:
            Clipboard.copy(path)
            popup(
                title="Signed data file created",
                text="The file has been copied to your clipboard.",
                thirdly_title=path,
                type="success",
            )

    def show_sign_dialog(self):
        self.sign_dialog = popup(
            title="Sign Data",
            target=self.sign_the_data,
            inputs=[["Data", False], ["Password", True]],
        )

    def verify_the_data(self):
        result = verify(self.verify_dialog.input_results["Path"])

        if result[0] == True:
            data_text = f"{result[1][:20]}..." if len(
                result[1]) > 20 else result[1]
            popup(
                title="Data is verified",
                text=f"The data is : {data_text}",
                thirdly_title=f"The sender is : {result[2]}",
                type="success",
            )
        else:
            popup(title="Data is not verified", type="failure")

    def show_verify_dialog(self):
        self.verify_dialog = popup(
            title="Verify Signed Data",
            target=self.verify_the_data,
            inputs=[["Path", False]],
        )

    def send_coin(self):
        try:
            GetBlock()
        except FileNotFoundError:
            popup(title="Please connect to an network.", type="failure")
            return False
        self.show_send_coin_dialog()

    def sign(self):
        self.show_sign_dialog()

    def verify(self):
        self.show_verify_dialog()

    def export_transaction_csv(self):
        if export_the_transactions():
            Clipboard.copy(MY_TRANSACTION_EXPORT_PATH)
            popup(
                title=
                f"CSV file created in {MY_TRANSACTION_EXPORT_PATH} directory, The directory has been copied to your clipboard.",
                type="success",
            )

        else:
            popup(title="You have not a transaction", type="warning")

    def callback_for_transaction_history_items(self, *args):
        the_signature_of_tx = args[0][:96]
        Clipboard.copy(the_signature_of_tx)
        popup(
            title=
            "The signature of transaction has been copied to your clipboard.",
            text=f"The signature is : {the_signature_of_tx}",
            type="success",
        )

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
            popup(title="You have not a transaction", type="warning")
