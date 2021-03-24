import unittest


class Test_Settings(unittest.TestCase):

    def test_creating_settings(self):
        temp_settings = the_settings()
        self.assertIsNotNone(temp_settings.test_mode(), "A problem on the test_mode.")
        self.assertIsNotNone(temp_settings.debug_mode(), "A problem on the debug_mode.")

    def test_saving_settings(self):
        temp_settings = the_settings()
        temp_test_mode = temp_settings.test_mode()
        temp_debug_mode = temp_settings.debug_mode()

        temp_settings.test_mode(True)
        temp_settings.debug_mode(True)

        temp_settings.save_settings()

        temp_test_settings = the_settings()
        self.assertEqual(temp_test_settings.test_mode(), True, "A problem on the saving the settings.")
        self.assertEqual(temp_test_settings.debug_mode(), True, "A problem on the saving the settings.")

        temp_settings.test_mode(False)
        temp_settings.debug_mode(False)

        temp_settings.save_settings()

        temp_test_settings = the_settings()
        self.assertEqual(temp_test_settings.test_mode(), False, "A problem on the saving the settings.")
        self.assertEqual(temp_test_settings.debug_mode(), False, "A problem on the saving the settings.")

        temp_settings.test_mode(temp_test_mode)
        temp_settings.debug_mode(temp_debug_mode)        


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from lib.settings import the_settings
    unittest.main()
