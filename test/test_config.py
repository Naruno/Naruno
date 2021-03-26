#!/usr/bin/python3
# -*- coding: utf-8 -*-
import unittest


class Test_Config(unittest.TestCase):

    def test_getting_and_saving_config(self):
        temp_config = get_config()
        self.assertIsNotNone(temp_config.main_folder, "A problem on the config.")

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from config import get_config
    unittest.main()
