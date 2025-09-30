from DATA.conexao import Conexao
from flask import session, flash

class Control:

    @staticmethod
    def exibir_itens():

        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        sql = """SELECT name, descripition, category, image, amount FROM tb_document"""

        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        mycursor.close()
        cx_db.close()

        return resultado