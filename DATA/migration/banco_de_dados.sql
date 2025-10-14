CREATE DATABASE IF NOT EXISTS db_tcc;
USE db_tcc;

CREATE TABLE IF NOT EXISTS tb_user (
    id_user INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    profile_type VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_document (
    id_document INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    doc_description VARCHAR(255) NOT NULL,
    category VARCHAR(15) NOT NULL,
    image VARCHAR(255) NOT NULL,
    amount INT NOT NULL
);

CREATE TABLE IF NOT EXISTS tb_historic (
    id_historic INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT,
    id_document INT,
    FOREIGN KEY (id_user) REFERENCES tb_user(id_user),
    FOREIGN KEY (id_document) REFERENCES tb_document(id_document),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tb_request (
    id_request INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT,
    id_document INT,
    FOREIGN KEY (id_user) REFERENCES tb_user(id_user),
    FOREIGN KEY (id_document) REFERENCES tb_document(id_document),
    status VARCHAR(15) DEFAULT 'solicitado'
);

CREATE TABLE IF NOT EXISTS tb_user_document (
    id_user_document INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT,
    id_document INT,
    FOREIGN KEY (id_user) REFERENCES tb_user(id_user),
    FOREIGN KEY (id_document) REFERENCES tb_document(id_document),
    CONSTRAINT unique_user_document UNIQUE(id_user, id_document)
);

CREATE TABLE IF NOT EXISTS tb_notification(
	id_notification INT PRIMARY KEY AUTO_INCREMENT,
    id_user INT,
    id_document INT,
	FOREIGN KEY (id_user) REFERENCES tb_user(id_user),
    FOREIGN KEY (id_document) REFERENCES tb_document(id_document)
);

-- Exemplo de inserções de dados

INSERT INTO tb_user (name, password, email, profile_type) VALUES ("zacajaca21", "12345678", "seuemail1@gmail.com", "master");
INSERT INTO tb_user (name, password, email, profile_type) VALUES ("zacajaca22", "12345678", "seuemail2@gmail.com", "common");
INSERT INTO tb_user (name, password, email, profile_type) VALUES ("zacajaca23", "12345678", "seuemail3@gmail.com", "common");

INSERT INTO tb_document (name, doc_description, category, image, amount) VALUES ("Prova de Matemática", "Esta prova possui 10 questões sobre matemática avançada", "matematica", "../../static/images/imagem_exemplo1.jpg", 10);
INSERT INTO tb_document (name, doc_description, category, image, amount) VALUES ("Prova de Química", "Esta prova possui 10 questões sobre química avançada", "quimica", "../../static/images/imagem_exemplo2.jpg", 15);
INSERT INTO tb_document (name, doc_description, category, image, amount) VALUES ("Prova de Biologia", "Esta prova possui 10 questões sobre biologia avançada", "biologia", "../../static/images/imagem_exemplo3.jpg", 20);

-- Corrigindo a junção entre as tabelas
SELECT * FROM tb_user
INNER JOIN tb_request ON tb_user.id_user = tb_request.id_user 
INNER JOIN tb_document ON tb_request.id_document = tb_document.id_document;

ALTER TABLE tb_request ADD COLUMN requested_amount INT NOT NULL DEFAULT 1;