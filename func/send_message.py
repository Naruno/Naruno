from func.send import send

from wallet.wallet import Wallet_Import

def send_message(message,to_user):
  my_public_key = Wallet_Import(0,0)
  my_private_key = Wallet_Import(0,1)

  if isinstance(message, str):
   send(my_public_key=my_public_key,my_private_key=my_private_key,to_user=to_user, data = message,amount=1)
  else:
    print("This is not text message.")