
from flask import Flask, render_template, redirect, request, session
from model import control_user
from model import control_document

app = Flask(__name__)

# CRIANDO CHAVE SECRETA
app.secret_key = "8350e5a3e24c153df2275c9f80692773"


@app.route("/")
def index():
    return render_template("pages/home.html")

@app.route("/logon")
def logon():
    return render_template("pages/logon.html")

@app.route("/api/documentos")
def documentos():
    itens = control_document.Control.exibir_itens()
    return render_template("pages/teste.html", itens = itens)

@app.route("/document/<codigo>")
def mostrar_documento(codigo):
    documento = control_document.Control.exibir_documento(codigo)
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return "Usuário não autenticado", 401


    if documento is None:
        return "Documento não encontrado", 404
    
    return render_template("pages/document.html", documento_html = documento, usuario_id = id_usuario)

@app.route("/document/pedido/<int:codigo>/<int:id_usuario>", methods=["POST"])
def registrar_pedido(codigo, id_usuario):
    try:
        control_user.Usuario.pedido_user(codigo, id_usuario)
        return "Pedido registrado com sucesso", 200
    except Exception as e:
        return f"Erro ao registrar pedido: {str(e)}", 500

@app.route("/post/logon", methods=["POST"])
def cadastro_user():
    nome = request.form.get("name")
    senha = request.form.get("password")
    email = request.form.get("email")

    sucesso = control_user.Usuario.registra_user(nome, senha, email)

    if sucesso:
        session['usuario_email'] = email
        return redirect("/")
    else:
        return redirect("/logon")


@app.route("/api/login", methods=["POST"])
def efetuar_login():
    email = request.form.get("email")
    senha = request.form.get("password")

    control_user.Usuario.login_user(email, senha)

    return redirect("/document/1")


# [ --------- FIM DAS ROTAS --------- ] #


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)