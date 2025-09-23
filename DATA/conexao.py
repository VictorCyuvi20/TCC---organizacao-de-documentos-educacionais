import mysql.connector

class Conexao:
    
    @staticmethod
    def cria_conexao():
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_tcc"
        )

        return mydb