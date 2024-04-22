import requests
import json
import dotenv
import os
dotenv.load_dotenv()
class Validation:
    def __init__(self,doc,tipo) -> None:
        self.doc  = doc
        self.tipo = tipo

    def valid(self):
        data = {}
        response = requests.get(f'https://my.apidev.pro/api/{self.tipo}/{self.doc}',headers = {
                    "Authorization":f'Bearer {os.getenv("TOKEN_DNI")}'
                })
        res=json.loads(response.text)
        if not (res['success']):
            data['error'] = res['message']
        else:
            data = res
        return data