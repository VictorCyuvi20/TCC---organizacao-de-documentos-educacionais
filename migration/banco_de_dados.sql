create database if not exists db_tcc;
use db_tcc;

create table if not exists tb_user(
	id_user int primary key auto_increment,
    name char(40) not null,
    password varchar(255) not null,
    email varchar(50) not null,
    profile_type char(15) not null
);

create table if not exists tb_document(
	id_document int primary key auto_increment,
    name char(40) not null,
    descripition char(255) not null,
    category char(15) not null,
    image text not null,
    amount int not null
);

create table if not exists tb_historic(
	id_historic int primary key auto_increment,
    -- Chaves Estrangeiras
    id_user int,
    id_document int,
    foreign key (id_user) references tb_user(id_user),
    foreign key (id_document) references tb_document(id_document),
    -- Data e Hora
    date_and_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

create table if not exists tb_request(
	id_request int primary key auto_increment,
    -- Chaves Estrangeiras
    id_user int,
    id_document int,
    foreign key (id_user) references tb_user(id_user),
    foreign key (id_document) references tb_document(id_document)
);

create table tb_user_document(
	id_user_document int primary key auto_increment,
    -- Chaves Estrangeiras
    id_user int,
    id_document int,
	foreign key (id_user) references tb_user(id_user),
    foreign key (id_document) references tb_document(id_document)
);

select * from tb_user;
insert into tb_user(name, password, email, profile_type) values("zacajaca21", "12345678", "seuemail1@gmail.com", "master");
insert into tb_user(name, password, email, profile_type) values("Cyuvi", "12345678", "seuemail2@gmail.com", "common");
insert into tb_user(name, password, email, profile_type) values("Skuar", "12345678", "seuemail3@gmail.com", "commun");

select * from tb_document;
insert into tb_document(name, descripition, category, image, amount) values("Prova de Matemática", "Esta prova possui 10 questões sobre matemática avançada", "matemática", "../../static/images/imagem_exemplo1.jpg", 10);
insert into tb_document(name, descripition, category, image, amount) values("Prova de Química", "Esta prova possui 10 questões sobre química avançada", "química", "../../static/images/imagem_exemplo3.jpg", 15);
insert into tb_document(name, descripition, category, image, amount) values("Prova de Biologia", "Esta prova possui 10 questões sobre biologia avançada", "biologia", "../../static/images/imagem_exemplo3.jpg", 20);

select * from tb_user inner join tb_document ON tb_user.id_user = tb_document.id_document
inner join tb_request ON tb_document.id_document = tb_request.id_document;
