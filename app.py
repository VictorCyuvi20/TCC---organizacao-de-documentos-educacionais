from flask import Flask, render_template, redirect

app = Flask(__name__)

# CRIANDO CHAVE SECRETA
app.secret_key = "8350e5a3e24c153df2275c9f80692773"


@app.route("/")
def index():
    return render_template("pages/login.html")

@app.route("/logon")
def logon():
    return render_template("pages/logon.html")

# [ --------- FIM DAS ROTAS --------- ] #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)