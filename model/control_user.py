from DATA.conexao import Conexao

class Control:

    def login_user(email, senha):
        cx_db = Conexao.cria_conexao()
        mycursor = cx_db.cursor(dictionary=True)

        valor = (email, senha)
        sql = """SELECT email, password, name FROM tb_user WHERE email = %s AND password = %s"""

        mycursor.execute(sql, valor)
        resultado = mycursor.fetchall()

        mycursor.close()

        return resultado
