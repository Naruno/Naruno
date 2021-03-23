import unittest


class Test_Wallet(unittest.TestCase):

    def test_creating_wallet(self):
        from wallet.wallet import Wallet_Create
        temp_private_key = Wallet_Create(save=False)
        result = True if "PRIVATE" in temp_private_key else False

        self.assertEqual(result, True, "A problem on the creating the wallet.")

    def test_saving_and_importing_the_wallet(self):
        from wallet.wallet import Wallet_Create , get_saved_wallet , Wallet_Import ,Wallet_Delete
        temp_private_key = Wallet_Create()

        saved_wallets = get_saved_wallet()
        
        result = False
        for each_wallet in saved_wallets:
            if temp_private_key == (each_wallet[1]).replace('\n', ''):
                if temp_private_key == (Wallet_Import((saved_wallets.index(each_wallet)),1)).replace('\n', ''):
                    result = True
                    Wallet_Delete(each_wallet)
                    break

        print(result)
        self.assertEqual(result, True, "A problem on the saving and importing the wallet.")

    #convert to pem or get from pem

if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    unittest.main()
