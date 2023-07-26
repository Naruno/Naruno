#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64
import contextlib
import hashlib
import os
import pickle
import time
import traceback
from datetime import datetime
from hashlib import sha256
from shutil import copy
from shutil import make_archive
from shutil import move
from shutil import rmtree
from shutil import unpack_archive
import random


force_compress = False
force_encrypt = False


class HASHES:
    cache = {}
    @staticmethod
    def get_hash(string: str, hash_type: str = "sha256") -> str:
        if string in HASHES.cache:
            return HASHES.cache[string]
        if hash_type == "sha256":
            result = sha256(string.encode()).hexdigest()
        elif hash_type == "sha512":
            result = sha512(string.encode()).hexdigest()
        elif hash_type == "md5":
            result = md5(string.encode()).hexdigest()
        else:
            raise ValueError("Hash type must be sha256, sha512 or md5")
        HASHES.cache[string] = result
        return result


class KOT:

    @staticmethod
    def benchmark_set(number: int = 10000,
                      compress: bool = False,
                      encryption_key: str = "") -> float:
        compress = True if force_compress else compress
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
            
        my_db = KOT("KOT-benchmark", self_datas=True)
        start = time.time()
        for i in range(number):
            my_db.set(
                "key" + str(i),
                "value" + str(i),
                compress=compress,
                encryption_key=encryption_key,
            )
        end = time.time()
        my_db.delete_all()
        return end - start

    @staticmethod
    def benchmark_get(
        number: int = 10000,
        compress: bool = False,
        encryption_key: str = "",
        dont_generate: bool = False,
    ) -> float:
        compress = True if force_compress else compress
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
        my_db = KOT("KOT-benchmark", self_datas=True)
        if not dont_generate:
            for i in range(number):
                my_db.set(
                    "key" + str(i),
                    "value" + str(i),
                    compress=compress,
                    encryption_key=encryption_key,
                )
        start = time.time()
        for i in range(number):
            my_db.get("key" + str(i), encryption_key=encryption_key)
        end = time.time()
        my_db.delete_all()
        return end - start

    @staticmethod
    def benchmark_delete(
        number: int = 10000,
        compress: bool = False,
        encryption_key: str = "",
        dont_generate: bool = False,
    ) -> float:
        compress = True if force_compress else compress
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
        my_db = KOT("KOT-benchmark", self_datas=True)
        if not dont_generate:
            for i in range(number):
                my_db.set(
                    "key" + str(i),
                    "value" + str(i),
                    compress=compress,
                    encryption_key=encryption_key,
                )
        start = time.time()
        for i in range(number):
            my_db.delete("key" + str(i))
        end = time.time()
        my_db.delete_all()
        return end - start

    @staticmethod
    def benchmark(number: int = 10000,
                  compress: bool = False,
                  encryption_key: str = "") -> float:
        compress = True if force_compress else compress
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
        total_time = 0
        total_time += KOT.benchmark_set(number, compress, encryption_key)
        total_time += KOT.benchmark_get(number,
                                        compress,
                                        encryption_key,
                                        dont_generate=True)
        total_time += KOT.benchmark_delete(number,
                                           compress,
                                           encryption_key,
                                           dont_generate=True)
        return total_time

    @staticmethod
    def database_list(folder: str = "") -> dict:
        database_index = KOT("KOT-database-index",
                             self_datas=True,
                             folder=folder)
        return database_index.dict()
    @staticmethod
    def gui(password, folder: str = ""):
        from .gui import GUI
        GUI(folder, password)


    @staticmethod
    def web(password, folder: str = "",host=None, port=0):
        from .gui import WEB
        WEB(folder, password, host, port)

    @staticmethod
    def database_delete(name: str, folder: str = "") -> bool:
        database_index = KOT("KOT-database-index",
                             self_datas=True,
                             folder=folder)
        try:
            the_db = KOT(name, folder=folder, self_datas=True)
            for each_key in the_db.get_all():
                the_db.delete(each_key)
            rmtree(database_index.get(name))
        except:
            return False

        database_index.delete(name)
        return True


    @staticmethod
    def database_pop(name: str, folder: str = "") -> bool:
        database_index = KOT("KOT-database-index",
                             self_datas=True,
                             folder=folder)
        try:
            the_db = KOT(name, folder=folder, self_datas=True)
            for each_key in the_db.get_all():
                the_db.delete(each_key)
        except:
            return False

        return True

    @staticmethod
    def database_delete_all(folder: str = ""):
        database_index = KOT("KOT-database-index",
                             self_datas=True,
                             folder=folder)

        for each_database in database_index.dict():
            KOT.database_delete(each_database, folder=folder)

    @staticmethod
    def database_pop_all(folder: str = ""):
        database_index = KOT("KOT-database-index",
                             self_datas=True,
                             folder=folder)

        for each_database in database_index.dict():
            KOT.database_pop(each_database, folder=folder)

    @staticmethod
    def database_rename(name: str,
                        new_name: str,
                        force: bool = False,
                        folder: str = "") -> bool:
        if new_name in KOT.database_list() and not force:
            return False
        try:
            first_db = KOT(name, folder=folder)
            location = first_db.backup(".")
            KOT.database_delete(name)
            second_db = KOT(new_name, folder=folder)
            second_db.restore(location)
            os.remove(location)
        except:
            traceback.print_exc()
            return False
        return True

    def __init__(self, name, self_datas: bool = False, folder: str = ""):
        self.name = name
        self.hashed_name = HASHES.get_hash(name)
        the_main_folder = os.getcwd() if not folder != "" else folder
        self.the_main_folder = the_main_folder
        self.location = os.path.join(the_main_folder,
                                     "KOT-" + self.hashed_name)

        if not self_datas:
            self.open_files_db = KOT("KOT-open_files_db",
                                     self_datas=True,
                                     folder=folder)
            database_index = KOT("KOT-database-index",
                                 self_datas=True,
                                 folder=folder)
            database_index.set(self.name, self.location)

        self.counter = 0

        self.cache = {}

        self.initialize()

    def initialize(self):
        try:
            os.makedirs(self.location)
        except OSError:
            if not os.path.isdir(self.location):
                raise

    def clear_cache(self):
        self.cache = {}
        for each_file in self.open_files_db.dict():
            if os.path.exists(each_file):
                os.remove(each_file)
        self.open_files_db.delete_all()

    def encrypt(self, key, message):
        from Crypto.Cipher import AES

        # Serializing the message
        message = pickle.dumps(message)
        # Turning to string
        message = base64.b64encode(message).decode("ascii")

        def pad(s):
            return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

        padded_message = pad(message)
        from Crypto import Random

        iv = Random.new().read(AES.block_size)
        cipher = AES.new(
            hashlib.sha256(key.encode()).digest(), AES.MODE_CBC, iv)
        return base64.b64encode(
            iv + cipher.encrypt(padded_message.encode())).decode()

    def decrypt(self, key, message):
        from Crypto.Cipher import AES

        def unpad(s):
            return s[:-ord(s[len(s) - 1:])]

        message = base64.b64decode(message.encode())
        iv = message[:AES.block_size]
        cipher = AES.new(
            hashlib.sha256(key.encode()).digest(), AES.MODE_CBC, iv)
        unpadded = unpad(cipher.decrypt(message[AES.block_size:])).decode()

        unpadded = base64.b64decode(unpadded)

        return pickle.loads(unpadded)

    def set(
        self,
        key: str,
        value=None,
        file: str = "",
        compress: bool = False,
        encryption_key: str = "",
        cache_policy: int = 0,
        dont_delete_cache: bool = False,
        dont_remove_file: bool = False,
        custom_key_location: str = "",
        short_cut: bool = False,
    ) -> bool:
        compress = True if force_compress else compress
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
        self.counter += 1

        meta = {"type": "value", "file": None, "direct_file": True}

        if not isinstance(key, str):
            raise TypeError("Key must be a string")
        if not isinstance(file, str):
            raise TypeError("File must be a string")

        try:
            standart_key_location = os.path.join(self.location,HASHES.get_hash(key))
            key_location =  standart_key_location if custom_key_location == "" else custom_key_location
            
            if custom_key_location != "" and not short_cut:
                self.set(key,value=key_location,file=file,compress=compress,encryption_key=encryption_key,cache_policy=cache_policy,dont_delete_cache=dont_delete_cache,dont_remove_file=dont_remove_file,short_cut = True)            

            key_location_loading = os.path.join(self.location,
                                                standart_key_location + ".l")
            random_number = random.randint(10000,99999)
            key_location_loading_indicator = os.path.join(
                self.location, standart_key_location + str(random_number) + ".li")

            key_location_reading_indicator = os.path.join(
                self.location, standart_key_location)
            key_location_compress_indicator = os.path.join(
                self.location, standart_key_location + ".co")

            if file != "":
                meta["type"] = "file"
                meta["file"] = os.path.join(
                    self.location, key_location + "." + file.split(".")[-1])
                try:
                    if not compress and encryption_key == "":
                        value = ""
                        if not dont_remove_file:
                            move(file, meta["file"])
                        else:
                            copy(file, meta["file"])
                    else:
                        meta["direct_file"] = False
                        with open(file, "rb") as f:
                            value = f.read()
                except:
                    traceback.print_exc()
                    return False

            if encryption_key != "":
                value = self.encrypt(encryption_key, value)

            the_dict = {"key": key, "value": value, "meta": meta, "short_cut": False}
            if short_cut:
                the_dict["short_cut"] = True

            if cache_policy != 0:
                the_dict["cache_time"] = time.time()
                the_dict["cache_policy"] = cache_policy
            else:
                if key in self.cache and not dont_delete_cache:
                    del self.cache[key]

            if compress:
                # create key_location_compress_indicator
                with open(key_location_compress_indicator, "wb") as f:
                    f.write(b"1")
                import mgzip

                with mgzip.open(key_location_loading, "wb") as f:
                    pickle.dump(the_dict, f)

            else:
                with open(key_location_loading, "wb") as f:
                    pickle.dump(the_dict, f)

            # Create a file that inform is loading
            with open(key_location_loading_indicator, "wb") as f:
                f.write(b"1")

            try_number = 0
            busy = True
            while not busy and try_number < 6:
                any_file = False
                for each_file in os.listdir(self.location):
                    if each_file.startswith(
                            key_location_reading_indicator) and each_file.endswith(
                                ".re"):
                        any_file = True
                if not any_file:
                    busy = False
                    break
                try_number += 1
                time.sleep(0.25)

            with contextlib.suppress(FileNotFoundError):
                move(key_location_loading, key_location)

            with contextlib.suppress(FileNotFoundError):
                os.remove(key_location_loading_indicator)

        except:
            traceback.print_exc()
            return False

        return True

    def set_withrkey(self, value) -> str:
        key = str(self.counter) + str(time.time())
        try:
            self.set(key, value)
            return key
        except:
            traceback.print_exc()
            return ""

    def transformer(self, element, encryption_key: str = ""):
        if "meta" not in element:
            element["meta"] = {"type": "value"}
        if "short_cut" not in element:
            element["short_cut"] = False
        if element["meta"]["type"] == "value":
            if encryption_key != "":
                return self.decrypt(encryption_key, element["value"])
            return element["value"]
        elif element["meta"]["type"] == "file":
            self.open_files_db.set(element["meta"]["file"], True)
            return element["meta"]["file"]


    def wait_system(self, key: str, indicator:str):
        try_number = 0
        busy = True
        while not busy and try_number < 6:
                any_file = False
                for each_file in os.listdir(self.location):
                    if each_file.startswith(
                            indicator) and each_file.endswith(
                                indicator):
                        any_file = True
                if not any_file:
                    busy = False
                    break
                try_number += 1
                time.sleep(0.25)



    def get(
        self,
        key: str,
        custom_key_location: str = "",
        encryption_key: str = "",
        no_cache: bool = False,
        raw_dict: bool = False,
        get_shotcut: bool = False,
    ):
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
        if key in self.cache and not no_cache:
            cache_control = False
            currently = time.time()
            last_time = self.cache[key]["cache_time"]
            cache_policy = self.cache[key]["cache_policy"]

            if currently - last_time < cache_policy:
                cache_control = True

            if cache_control:
                return self.transformer(self.cache[key])


        standart_key_location = os.path.join(self.location,HASHES.get_hash(key))
        key_location =  standart_key_location if custom_key_location == "" else custom_key_location
            
        
        key_location_loading_indicator = os.path.join(
                self.location, standart_key_location)

        random_number = random.randint(10000,99999)
        key_location_reading_indicator = os.path.join(
                self.location, standart_key_location +str(random_number) + ".re")
        key_location_compress_indicator = os.path.join(
                self.location, standart_key_location + ".co")



        try_number = 0
        busy = True
        while not busy and try_number < 6:
                any_file = False
                for each_file in os.listdir(self.location):
                    if each_file.startswith(
                            key_location_loading_indicator) and each_file.endswith(
                                ".li"):
                        any_file = True
                if not any_file:
                    busy = False
                    break
                try_number += 1
                time.sleep(0.25)


        if not os.path.isfile(key_location):
            return None

        total_result = None
        total_result_standart = None

        try:

            # Create a file that inform is reading
            with contextlib.suppress(Exception):
                with open(key_location_reading_indicator, "wb") as f:
                    f.write(b"1")

            # Read the file
            if os.path.exists(key_location_compress_indicator):
                import mgzip
                with mgzip.open(key_location,
                                "rb") as f:
                    result = pickle.load(f)
            else:
                with open(key_location,
                          "rb") as f:
                    result = pickle.load(f)

            # Transform the result
            total_result_standart = result
            try:
                total_result = self.transformer(result, encryption_key=encryption_key)
            except TypeError:
                traceback.print_exc()
                total_result = result            

            # Add to cache
            if "cache_time" in total_result_standart:
                self.cache[key] = total_result_standart

        except EOFError or FileNotFoundError:
            traceback.print_exc()

        # Delete the file that inform is reading
        if os.path.isfile(key_location_reading_indicator):
            with contextlib.suppress(Exception):
                os.remove(key_location_reading_indicator)

        # Create the file if there is an compress or encryption situation
        if total_result_standart["meta"]["type"] == "file":
            if not total_result_standart["meta"]["direct_file"]:
                with open(total_result_standart["meta"]["file"], "wb") as f:
                    the_bytes = total_result_standart["value"]
                    if encryption_key != "":
                        the_bytes = self.decrypt(encryption_key, the_bytes)
                    f.write(the_bytes)

        # Return the result
        if raw_dict:

            if total_result_standart["short_cut"] and not get_shotcut:
                total_result_standart = self.get(key, custom_key_location=total_result_standart["value"],
                                    encryption_key=encryption_key,
                                    no_cache=no_cache,
                                    raw_dict=raw_dict)


            return total_result_standart



        if total_result_standart["short_cut"] and not get_shotcut:
            total_result = self.get(key, custom_key_location=total_result_standart["value"],
                                    encryption_key=encryption_key,
                                    no_cache=no_cache,
                                    raw_dict=raw_dict)


        return total_result

    def get_key(self, key_location: str):
        key_location_compress_indicator = os.path.join(self.location,
                                                       key_location + ".co")
        if not os.path.isfile(os.path.join(self.location, key_location)):
            return None
        total_result = None

        try:
            if os.path.exists(key_location_compress_indicator):
                import mgzip
                with mgzip.open(os.path.join(self.location, key_location),
                                "rb") as f:
                    result = pickle.load(f)
            else:
                with open(os.path.join(self.location, key_location),
                          "rb") as f:
                    result = pickle.load(f)


            if not "cache_time" in result:
                result["cache_time"] = 0
            if not "cache_policy" in result:
                result["cache_policy"] = 0
            if not "meta" in result:
                result["meta"] = {"type": "value"}
            try:
                total_result = result["key"]
            except TypeError:
                total_result = False


        except EOFError or FileNotFoundError:
            pass
        return total_result

    def get_all(self):
        return self.dict()


    def get_count(self):
        return len(self.dict(no_data=True))

    def delete(self, key: str) -> bool:
        try:
            if key in self.cache:
                del self.cache[key]
            key_location = os.path.join(self.location,
                                        HASHES.get_hash(key))
            key_location_compress_indicator = os.path.join(
                self.location, key_location + ".co")

            with contextlib.suppress(TypeError):
                maybe_file = self.get(key)
                if os.path.exists(maybe_file):
                    os.remove(maybe_file)

            the_get = self.get(key, no_cache=True, raw_dict=True, get_shotcut=True)
            if the_get["short_cut"]:
                with contextlib.suppress(TypeError):
                    maybe_file = self.get(key, custom_key_location=the_get["value"])
                    if os.path.exists(maybe_file):
                        os.remove(maybe_file)
                os.remove(the_get["value"])             

            if os.path.exists(key_location_compress_indicator):
                os.remove(
                    os.path.join(self.location,
                                 key_location_compress_indicator))
            if os.path.exists(os.path.join(self.location, key_location)):
                os.remove(os.path.join(self.location, key_location))
        except:
            traceback.print_exc()
            return False

        return True

    def delete_all(self) -> bool:
        try:
            for key in self.dict():
                self.delete(key)
        except:
            traceback.print_exc()
            return False
        return True

    def dict(self, encryption_key: str = "", no_data: bool = False):
        encryption_key = force_encrypt if force_encrypt != False else encryption_key
        result = {}
        for key in os.listdir(self.location):
            if not "." in key:
                the_key = self.get_key(key)
                if not the_key is None:
                    if the_key != False:
                        result_of_key = (self.get(
                            the_key, encryption_key=encryption_key)
                                         if not no_data else True)
                        if not result_of_key is None:
                            result[the_key] = result_of_key
        return result

    def size_all(self) -> int:
        # Calculate self.location size
        total_size = 0

        for dirpath, dirnames, filenames in os.walk(self.location):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

        return total_size

    def size(self, key: str) -> int:
        total_size = 0
        try:
            key_location = os.path.join(self.location,
                                        HASHES.get_hash(key))

            key_location_compress_indicator = os.path.join(
                self.location, key_location + ".co")

            if os.path.exists(key_location_compress_indicator):
                total_size += os.path.getsize(
                    os.path.join(self.location, key_location + ".co"))

            with contextlib.suppress(TypeError):
                maybe_file = self.get(key)
                if os.path.exists(maybe_file):
                    total_size += os.path.getsize(maybe_file)

            total_size += os.path.getsize(
                os.path.join(self.location, key_location))
        except:
            traceback.print_exc()

        return total_size

    def backup(self, backup_location: str) -> str:
        # create a name for backup that a date
        name = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        location = os.path.join(backup_location, name)
        make_archive(location, "zip", self.location)
        move(location + ".zip", location + ".KOT")
        return location + ".KOT"

    def restore(self, backup_location: str) -> bool:
        try:
            move(backup_location, backup_location.replace(".KOT", ".zip"))
            backup_location = backup_location.replace(".KOT", ".zip")
            unpack_archive(backup_location, self.location)
            move(backup_location, backup_location.replace(".zip", ".KOT"))
            return True
        except:
            traceback.print_exc()
            return False





def main():
    import fire

    fire.Fire(KOT)
