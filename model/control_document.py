from DATA.conexao import Conexao
from flask import session, flash

class Control:

    @staticmethod
    def exibir_itens():

        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        sql = """SELECT id_document, name, descripition, category, image, amount FROM tb_document"""

        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        mycursor.close()
        cx_db.close()

        return resultado
    
    @staticmethod
    def exibir_documento(codigo):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        sql = """SELECT * from tb_document WHERE id_document = %s"""

        mycursor.execute(sql, (codigo,))
        documento = mycursor.fetchone()

        mycursor.close()
        cx_db.close()

        return documento
    
    @staticmethod
    def exibir_historico(id_usuario, search_query=""):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        # Consulta simples para filtrar pelo nome do documento
        sql = """SELECT h.*, d.name as document_name
                FROM tb_historic h
                JOIN tb_document d ON h.id_document = d.id_document
                WHERE h.id_user = %s AND d.name LIKE %s"""
        
        # Usando %search_query% para correspondência parcial no nome do documento
        mycursor.execute(sql, (id_usuario, f"%{search_query}%"))
        resultado = mycursor.fetchall()

        mycursor.close()
        cx_db.close()

        return resultado


