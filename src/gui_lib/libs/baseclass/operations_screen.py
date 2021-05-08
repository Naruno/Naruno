#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


import os

class OperationScreen(MDScreen):
    pass

class Send_Coin_Box(MDGridLayout):
    cols = 2
    pass

class OperationBox(MDGridLayout):
    cols = 2
    send_coin_dialog = None
    FONT_PATH = f"{os.environ['DECENTRA_ROOT']}/gui_lib/fonts/"


    def show_send_coin_dialog(self):
        if not self.send_coin_dialog:
            self.send_coin_dialog = MDDialog(
                title="Send Coin",
                type="custom",
                auto_dismiss=False,
                content_cls=Send_Coin_Box(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_press=self.dismiss_send_coin_dialog,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
                    ),
                    MDFlatButton(
                        text="OK",
                        on_press=self.sent_the_coins,
                        font_size= "18sp",
                        font_name= self.FONT_PATH + "RobotoCondensed-Bold",
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
    def sent_the_coins(self,widget):
        from func.send_coin import send_coin

        text_list = self.get_send_coin_dialog_text()
        receiver_adress = text_list[1]
        amount = text_list[0]

        print(receiver_adress)
        print(amount)


        send_coin(float(amount), receiver_adress)

        

        self.send_coin_dialog.dismiss()
    def dismiss_send_coin_dialog(self,widget):
        self.get_send_coin_dialog_text()

        self.send_coin_dialog.dismiss()

    def send_coin(self):
        self.show_send_coin_dialog()

