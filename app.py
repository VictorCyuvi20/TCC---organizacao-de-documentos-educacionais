
from flask import Flask, render_template, redirect, request, session
from model import control_user

app = Flask(__name__)

# CRIANDO CHAVE SECRETA
app.secret_key = "8350e5a3e24c153df2275c9f80692773"


@app.route("/")
def index():
    return render_template("pages/login.html")

@app.route("/logon")
def logon():
    return render_template("pages/logon.html")


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
    return redirect("/")
# [ --------- FIM DAS ROTAS --------- ] #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)