from DATA.conexao import Conexao
from hashlib import sha256
from flask import session, flash


class Usuario:

    @staticmethod
    def login_user(email, senha):
        # Criptografando a senha
        senha_criptografada = sha256(senha.encode()).hexdigest()

        # Usa a classe Conexao para obter a conexão
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        try:
            # Consulta para verificar o usuário com o email e senha
            sql = """SELECT id_user, email, name, profile_type FROM tb_user WHERE email = %s AND password = %s"""
            mycursor.execute(sql, (email, senha_criptografada))

            # Pega o primeiro resultado
            resultado = mycursor.fetchone()

            # Se encontrar o usuário, armazena os dados na sessão
            if resultado:
                session['email_usuario'] = resultado['email']
                session['nome_usuario'] = resultado['name']
                session['id_usuario'] = resultado['id_user']
                session['profile_type'] = resultado['profile_type']
                return True
            else:
                return False
        except Exception as err:
            print(f"Erro no banco de dados: {err}")
            return False
        finally:
            # Fechando o cursor e a conexão
            if mycursor:
                mycursor.close()
            if cx_db:
                cx_db.close()

        
    @staticmethod
    def registra_user(nome, senha, email):
        try:
            senha_criptografada = sha256(senha.encode()).hexdigest()

            cx_db = Conexao.cria_conexao()
            if cx_db is None:
                flash("Erro! Talvez a conexão com o banco de dados tenha falhado. Atualize a página e tente novamente")
                return False
            
            mycursor = cx_db.cursor()


            sql = """INSERT INTO tb_user (name, password, email, profile_type) VALUES (%s, %s, %s, 'common')"""

            valores = (nome, senha_criptografada, email, )

            mycursor.execute(sql, valores)
            cx_db.commit()

            return True

        finally:
            try:
                if mycursor:
                    mycursor.close()
                if cx_db:
                    cx_db.close()
            except:
                pass

    def pedido_user(codigo, id_usuario):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor()

        sql = """INSERT INTO tb_historic (id_user, id_document) VALUES (%s, %s)"""

        sql2 = """INSERT INTO tb_request (id_user, id_document) VALUES (%s, %s)"""

        mycursor.execute(sql, (id_usuario, codigo))
        mycursor.execute(sql2, (id_usuario, codigo))

        cx_db.commit()

        mycursor.close()
        cx_db.close()

