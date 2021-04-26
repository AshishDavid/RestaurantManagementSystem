CREATE DATABASE IF NOT EXISTS geeklogin
DEFAULT CHARACTER SET utf8
DEFAULT COLLATE utf8_general_ci;
USE geeklogin;

CREATE TABLE IF NOT EXISTS accounts (
     id int(11) NOT NULL AUTO_INCREMENT,
     username varchar(50) NOT NULL,
     password varchar(255) NOT NULL,
     email varchar(100) NOT NULL,
     PRIMARY KEY (id)
) Engine=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS dishes (
	id int(11) NOT NULL AUTO_INCREMENT,
    name varchar(50) NOT NULL,
    code varchar(50) NOT NULL,
    quantity int(50) NOT NULL,
    price double NOT NULL,
    PRIMARY KEY(id)
)Engine=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

 INSERT INTO dishes (id, name, code, quantity, price) VALUES
(1, 'dish1', 'D0001', 1, 12000.00),
(2, 'dish2', 'D0002', 1, 5000.00),
(3, 'dish3', 'D0003', 1, 1000.00),
(4, 'dish4', 'D0004', 1, 80000.00),
(5, 'dish5', 'D0005', 1, 150000.00),
(6, 'dish6', 'D0006', 1, 3000.00),
(7, 'dish7', 'D0007', 1, 3000.00),
(8, 'dish8', 'D0008', 1, 400.00);