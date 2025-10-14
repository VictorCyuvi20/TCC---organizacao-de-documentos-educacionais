from flask import Flask, render_template, redirect, request, session, flash
from model import control_user 
from model import control_document
import re

app = Flask(__name__)

# CRIANDO CHAVE SECRETA
app.secret_key = "8350e5a3e24c153df2275c9f80692773"

# ROTAS PARA CARREGAR PÁGINAS

#rota para a pagina principal
@app.route("/")
def pag_login():

    if 'id_usuario' in session:
        itens = control_document.Control.exibir_itens()
        return render_template("pages/home.html", itens=itens)
    
    return render_template("pages/login.html")

#rota para à pagina de cadastro
@app.route("/logon")
def logon():
    return render_template("pages/logon.html")

#rota para a pagina onde é possivel ver os documentos cadastrados
@app.route("/documentos")
def documentos():

    if 'id_usuario' not in session:
        flash("Você precisa fazer login para acessar os documentos")
        return redirect("/")

    itens = control_document.Control.exibir_itens()
    return render_template("pages/home.html", itens=itens)

@app.route("/historico", methods=["GET"])
def historico():
    # Recuperando o ID do usuário da sessão
    id_usuario = session.get('id_usuario')
    
    if id_usuario is None:
        return "Usuário não autenticado", 401  # Se não tiver id_usuario na sessão, exibe erro

    search_query = request.args.get('search', '')  # Pegando a pesquisa da URL, se houver
    # Chama a função exibir_historico para pegar os dados
    id_usuario_data = control_document.Control.exibir_historico(id_usuario, search_query)

    # Se não houver dados, retorna uma mensagem de erro
    if not id_usuario_data:
        return "Nenhum histórico encontrado", 404

    # Renderiza o template 'user_requests.html' com os dados encontrados
    return render_template("pages/user_requests.html", id_usuario_html=id_usuario_data)

#rota para a pagina do documento escolhido para a solicitação
@app.route("/document/<codigo>")
def mostrar_documento(codigo):
    documento = control_document.Control.exibir_documento(codigo)
    id_usuario = session.get('id_usuario')

    if id_usuario is None:
        return "Usuário não autenticado", 401


    if documento is None:
        return "Documento não encontrado", 404
    
    return render_template("pages/document.html", documento_html = documento, usuario_id = id_usuario)

@app.route("/adm_request")
def adm_request():
    # Verifica se o usuário está logado
    if 'id_usuario' not in session:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect("/")

    # Verifica se é administrador
    if session.get('profile_type') != 'master':
        flash("Acesso negado: você não tem permissão para acessar essa página.", "error")
        return redirect("/documentos")

    # Usuário é master → carrega solicitações
    todas_solicitacoes = control_document.Control.exibir_todas_solicitacoes()
    return render_template("pages/adm_requests.html", solicitacoes_html=todas_solicitacoes)

@app.route("/user_profile")
def user_profile():
    return render_template("pages/user_profile.html")

@app.route("/atividade")
def atividade():
    return render_template("pages/atividade.html")

# -------------ROTAS QUE PRECISAM CARREGAR ALGO-------------

#rota para efetuar o cadastro do usuario na tabela do banco de dados (tb_user)
@app.route("/api/logon", methods=["POST"])
def cadastro_user():
    nome = request.form.get("name")
    senha = request.form.get("password")
    email = request.form.get("email")

    # Valida o formato do email
    if not validar_email(email):
        flash("O formato do email é inválido.", "error")  # Exibe mensagem de erro
        return redirect("/logon")  # Redireciona de volta para a página de cadastro

    # Aqui você pode adicionar a lógica para verificar se o email já existe (caso precise)

    sucesso = control_user.Usuario.registra_user(nome, senha, email)

    if sucesso:
        session['usuario_email'] = email  # Armazena o email na sessão
        return redirect("/")  # Redireciona para a página inicial após cadastro
    else:
        flash("Erro ao criar conta. Tente novamente.", "error")  # Exibe mensagem de erro
        return redirect("/logon")  # Redireciona de volta para a página de cadastro


def validar_email(email):
    # Expressão regular para validar o formato do email
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Retorna True se o email corresponder ao padrão, senão retorna False
    return re.match(padrao_email, email) is not None


#rota para validar o login do usuario (a validação esta no control user na função "login_user")
@app.route("/api/login", methods=["POST"])
def efetuar_login():
    email = request.form.get("email")
    senha = request.form.get("password")

    if not validar_email(email):
        flash("Email inválido.")
        return redirect("/")

    usuario = control_user.Usuario.login_user(email, senha)

    if usuario:
        return redirect("/documentos")
    
    else:
        flash("Email ou senha incorreta")
        return redirect("/")

#rota para adicionar os pedidos nas tabelas do banco de dados, tanto no request quanto no historic
@app.route("/api/document/pedido/<int:codigo>/<int:id_usuario>", methods=["POST"])
def registrar_pedido(codigo, id_usuario):
    try:
        quantidade = int(request.form.get("quantity"))

        if quantidade < 1:
            flash("Quantidade inválida.", "error")
            return redirect(f"/document/{codigo}")

        control_user.Usuario.pedido_user(codigo, id_usuario, quantidade)

        flash("Pedido enviado ao administrador.", "success")
        return redirect("/historico")

    except Exception as e:
        flash(f"Erro ao registrar pedido: {str(e)}", "error")
        return redirect("/documentos")

    
@app.route("/api/request/aprovar/<int:id_request>", methods=["POST"])
def aprovar_solicitacao(id_request):
    try:
        control_user.Usuario.aprovar_pedido(id_request)
        flash("Solicitação aprovada com sucesso!", "success")
        return redirect("/adm_request")
    except Exception as e:
        flash(f"Erro ao aprovar solicitação: {str(e)}", "error")
        return redirect("/adm_request")

@app.route("/api/request/cancelar/<int:id_request>", methods=["POST"])
def cancelar_pedido(id_request):
    try:
        control_user.Usuario.cancelar_pedido(id_request)
        flash("Solicitação cancelada com sucesso.", "success")
        return redirect("/historico")
    except Exception as e:
        flash(f"Erro ao cancelar solicitação: {str(e)}", "error")
        return redirect("/historico")
    





# [ --------- FIM DAS ROTAS --------- ] #

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)