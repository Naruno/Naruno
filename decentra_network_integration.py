import requests

class Integration:
  cache = []

  def send(action, app_data, password, to_user) -> bool:
    data = {
      "action": action,
      "data": app_data
    }

    request_body = {
      "password": password,
      "to_user": to_user,
      "data": data,  
    }

    response = requests.post('http://localhost:8000/send/', data=request_body)

    return response.text




  def get():

    response = requests.get('http://localhost:8000/export/transactions/json')
    transactions = response.json()

    for transaction in transactions:
      if transaction in Integration.cache:
        transactions.remove(transaction)
      else:
        Integration.cache.append(transaction)
    for transaction in transactions:
      if transaction["data"]["action"] == "app_name_action_name":
        print(transaction["data"])


print(Integration.send(
  action="app_name_action_name",
  app_data="Hello World",
  password="123",
  to_user="Decentra-Network-00000000000000000000002"
))