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
                return resultado
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

    @staticmethod
    def pedido_user(codigo, id_usuario, quantidade):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor()

        try:
            # Verifica o estoque atual
            sql_estoque = "SELECT amount FROM tb_document WHERE id_document = %s"
            mycursor.execute(sql_estoque, (codigo,))
            resultado = mycursor.fetchone()

            if resultado is None:
                raise Exception("Documento não encontrado.")

            estoque_atual = resultado[0]

            if quantidade > estoque_atual:
                raise Exception("Quantidade solicitada maior do que o disponível em estoque.")

            # Registra nos históricos e pedidos
            sql_historico = """INSERT INTO tb_historic (id_user, id_document) VALUES (%s, %s)"""
            sql_request = """INSERT INTO tb_request (id_user, id_document, requested_amount) VALUES (%s, %s, %s)"""
            mycursor.execute(sql_historico, (id_usuario, codigo))
            mycursor.execute(sql_request, (id_usuario, codigo, quantidade))

            # Atualiza estoque
            novo_estoque = estoque_atual - quantidade
            sql_update_estoque = """UPDATE tb_document SET amount = %s WHERE id_document = %s"""
            mycursor.execute(sql_update_estoque, (novo_estoque, codigo))

            cx_db.commit()

        except Exception as erro:
            cx_db.rollback()
            raise erro

        finally:
            mycursor.close()
            cx_db.close()


    @staticmethod
    def aprovar_pedido(id_request):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor()

        sql = "UPDATE tb_request SET status = 'aprovado' WHERE id_request = %s"
        mycursor.execute(sql, (id_request,))
        cx_db.commit()

        mycursor.close()
        cx_db.close()


    @staticmethod
    def cancelar_pedido(id_request):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor()

        try:
            # 1. Buscar dados da solicitação
            sql_select = """SELECT id_document, requested_amount FROM tb_request WHERE id_request = %s"""
            mycursor.execute(sql_select, (id_request,))
            resultado = mycursor.fetchone()

            if not resultado:
                raise Exception("Solicitação não encontrada.")

            id_document = resultado[0]
            quantidade = resultado[1]

            # 2. Atualizar o estoque somando de volta a quantidade
            sql_update = """UPDATE tb_document SET amount = amount + %s WHERE id_document = %s"""
            mycursor.execute(sql_update, (quantidade, id_document))

            # 3. Deletar a solicitação da tabela tb_request
            sql_delete = """DELETE FROM tb_request WHERE id_request = %s"""
            mycursor.execute(sql_delete, (id_request,))

            cx_db.commit()

        except Exception as e:
            cx_db.rollback()
            raise e

        finally:
            mycursor.close()
            cx_db.close()

    @staticmethod
    def buscar_tipo_usuario(email):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor()

        sql = "SELECT profile_type FROM tb_user WHERE email = %s"
        mycursor.execute(sql, (email,))
        resultado = mycursor.fetchone()

        mycursor.close()
        cx_db.close()

        if resultado:
            return resultado[0]
        return None

