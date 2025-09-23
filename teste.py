#para testar login cadastro ou outras coisas do banco de dados

from model.control_user import login_user

if __name__ == "__main__":
    print(login_user("seuemail2@gmail.com", "12345678"))