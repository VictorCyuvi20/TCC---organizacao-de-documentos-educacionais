from DATA.conexao import Conexao
from flask import session, flash

class Control:

    @staticmethod
    def exibir_itens():

        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        sql = """SELECT id_document, name, doc_description, category, image, amount FROM tb_document"""

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
        sql = """
        SELECT r.*, d.name as document_name, d.image
        FROM tb_request r
        JOIN tb_document d ON r.id_document = d.id_document
        WHERE r.id_user = %s AND d.name LIKE %s
        ORDER BY r.id_request DESC
        """

        
        # Usando %search_query% para correspondência parcial no nome do documento
        mycursor.execute(sql, (id_usuario, f"%{search_query}%"))
        resultado = mycursor.fetchall()

        mycursor.close()
        cx_db.close()

        return resultado

    @staticmethod
    def exibir_todas_solicitacoes():
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        sql = """
            SELECT r.id_request, r.id_user, r.id_document, r.status, r.requested_amount,
                u.name AS user_name, d.name AS document_name, d.image, d.amount AS estoque_atual
            FROM tb_request r
            JOIN tb_user u ON r.id_user = u.id_user
            JOIN tb_document d ON r.id_document = d.id_document
        """
        mycursor.execute(sql)
        resultado = mycursor.fetchall()

        mycursor.close()
        cx_db.close()

        return resultado

