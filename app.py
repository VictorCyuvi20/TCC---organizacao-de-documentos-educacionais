from flask import Flask, render_template, redirect

app = Flask(__name__)

# CRIANDO CHAVE SECRETA
app.secret_key = "8350e5a3e24c153df2275c9f80692773"


@app.route("/")
def pagina_principal():

    return render_template(".html")