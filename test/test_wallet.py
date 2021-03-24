import unittest


class Test_Wallet(unittest.TestCase):

    def test_saving_and_importing_the_wallet(self):
        temp_private_key_class = Wallet_Create()
        temp_private_key = temp_private_key_class.toPem().replace('\n', '')

        saved_wallets = get_saved_wallet()
        
        result = False
        for each_wallet in saved_wallets:
            if temp_private_key == (each_wallet[1]).replace('\n', ''):
                if temp_private_key == (Wallet_Import((saved_wallets.index(each_wallet)),1)).replace('\n', ''):
                    result = True
                    Wallet_Delete(each_wallet)
                    break

        result = True if "PRIVATE" in temp_private_key else False
        self.assertEqual(result, True, "A problem on the saving and importing the wallet.")



    def test_Private_Pem_Conversion(self):
        temp_private_key_class = Wallet_Create(save=False)
        pem = temp_private_key_class.toPem()
        privateKey2 = PrivateKey.fromPem(pem)
        self.assertEqual(temp_private_key_class.secret, privateKey2.secret)
        self.assertEqual(temp_private_key_class.curve, privateKey2.curve)



    def test_Public_Conversion(self):
        privateKey = Wallet_Create(save=False)
        publicKey1 = privateKey.publicKey()
        pem = publicKey1.toPem()
        publicKey2 = PublicKey.fromPem(pem)
        self.assertEqual(publicKey1.point.x, publicKey2.point.x)
        self.assertEqual(publicKey1.point.y, publicKey2.point.y)
        self.assertEqual(publicKey1.curve, publicKey2.curve)


if __name__ == '__main__':
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
    from wallet.wallet import Wallet_Create, get_saved_wallet, Wallet_Import, Wallet_Delete, PrivateKey, toBytes, PublicKey
    unittest.main()
