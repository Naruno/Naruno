#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import contextlib
import json
import os
from hashlib import sha256

import requests

from naruno.lib.config_system import get_config
from naruno.lib.settings_system import the_settings


class Integration:

    def __init__(
        self,
        app_name,
        host="0.0.0.0",
        port=8000,
        password="123",
        sended=True,
        sended_not_validated=False,
        cache_true=True,
    ):
        """
        :param host: The host of the node
        :param port: The port of the node
        :param password: The password of the wallet
        """
        self.app_name = app_name
        self.cache_name = sha256(self.app_name.encode()).hexdigest()
        self.host = host
        self.port = port
        self.password = password

        self.sended = sended

        self.sended_not_validated = sended_not_validated

        self.cache_true = cache_true

        self.get_cache()

    def disable_cache(self):
        self.cache_true = False
        self.cache = []

    def get_cache(self):
        if self.cache_true == False:
            self.cache = []
            return

        os.chdir(get_config()["main_folder"])

        if not os.path.exists(f"db/remote_app_cache/{self.cache_name}.cache"):
            self.cache = []
            self.save_cache()
        with open(f"db/remote_app_cache/{self.cache_name}.cache",
                  "r") as cache:
            self.cache = json.load(cache)

    def save_cache(self):
        os.chdir(get_config()["main_folder"])
        with open(f"db/remote_app_cache/{self.cache_name}.cache",
                  "w") as cache:
            json.dump(self.cache, cache)

    def delete_cache(self):
        os.chdir(get_config()["main_folder"])
        os.remove(f"db/remote_app_cache/{self.cache_name}.cache")

    def prepare_request(self, end_point, type, data=None) -> requests.Response:
        """
        :param end_point: The end point of the request
        :param type: The type of the request (get, post)
        :param data: The data of the request
        :return: The response of the request
        """
        api = f"http://{self.host}:{self.port}"
        response = None
        if type == "post":
            response = requests.post(api + end_point, data=data)
        elif type == "get":
            response = requests.get(api + end_point)

        return response

    def send(self, action, app_data, to_user) -> bool:
        """
        :param action: The action of the app
        :param app_data: The data of the app
        :param to_user: The user to send the data to
        """
        data = {"action": self.app_name + action, "app_data": app_data}

        data = json.dumps(data)

        request_body = {
            "password": self.password,
            "to_user": to_user,
            "data": data,
        }
        response = self.prepare_request("/send/",
                                        type="post",
                                        data=request_body)

        return False if "false" in response.text else True

    def get(self):
        backup_host = copy.copy(self.host)
        backup_port = copy.copy(self.port)
        if the_settings()["baklava"]:
            self.host = "test_net.1.naruno.org"
            self.port = 8000

        response = self.prepare_request("/transactions/received", type="get")
        transactions = response.json()
        transactions_sended = {}
        transactions_sended_not_validated = {}

        if self.sended:
            response = self.prepare_request("/transactions/sended/validated",
                                            type="get")
            transactions_sended = response.json()

        if self.sended_not_validated:
            response = self.prepare_request(
                "/transactions/sended/not_validated", type="get")
            transactions_sended_not_validated = response.json()

        new_dict = {}

        for transaction in transactions:
            if transaction in self.cache:
                continue
            else:
                new_dict[transaction] = transactions[transaction]
                self.cache.append(transaction)

        for transaction in transactions_sended:
            if transaction in self.cache:
                continue
            else:
                new_dict[transaction] = transactions_sended[transaction]
                self.cache.append(transaction)

        for transaction in transactions_sended_not_validated:
            if transaction in self.cache:
                continue
            else:
                new_dict[transaction] = transactions_sended_not_validated[
                    transaction]
                self.cache.append(transaction)

        self.save_cache()

        result = []

        for transaction in new_dict:
            if not new_dict[transaction]["transaction"]["data"] == "NP":
                with contextlib.suppress(json.decoder.JSONDecodeError):
                    new_dict[transaction]["transaction"]["data"] = json.loads(
                        new_dict[transaction]["transaction"]["data"])
                    
                    if self.app_name in new_dict[transaction]["transaction"]["data"][
                            "action"]:
                        result.append(new_dict[transaction]["transaction"])

        self.host = backup_host
        self.port = backup_port

        return result
