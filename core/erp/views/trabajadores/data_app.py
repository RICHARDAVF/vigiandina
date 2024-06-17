from dotenv import load_dotenv
import pyodbc
import os
load_dotenv()
class Connect:
    def __init__(self,sql,params):
        self.sql = sql
        self.params = params
        self.result = self.query()
    def query(self):
        host = os.getenv("HOST")
        bdname = os.getenv("BDNAME")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' +
                               host+';DATABASE='+bdname+';UID='+username+';PWD=' + password)
        data = {}
        try:
            cursor = conn.cursor()
            cursor.execute(self.sql,self.params)
            datos = cursor.fetchall()

        except Exception as e:
            data["error"] = f"Ocurrio un error {str(e)}"
        return data
    def __call__(self):
        return self.result