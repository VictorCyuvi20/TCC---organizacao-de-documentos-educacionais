from flask import Flask, render_template, redirect

app = Flask(__name__)

# CRIANDO CHAVE SECRETA
app.secret_key = "SLAIRMAO"


@app.route("/")
def pagina_principal():

    return render_template(".html")