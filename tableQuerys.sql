create database RegChat
use RegChat

create table users(
	id_user int identity(1,1) primary key not null,
	username varchar(30),
	passw varchar(20)
);

create table chatroom(
	id_chat int identity(1,1) primary key not null,
	chatname varchar(50)
)

create table membersCR(
	id_user int not null,
	id_chat int not null,
	role varchar(20) not null
)