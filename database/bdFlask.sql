CREATE TABLE usuario(
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	apellido varchar(255) NOT NULL,
	username varchar(255) NOT NULL,
	pass varchar(255) NOT NULL
);

CREATE TABLE alias(
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	apellido varchar(255) NOT NULL,
	cod_alias varchar(255) NOT NULL
);

CREATE TABLE documento(
	id INT NOT NULL PRIMARY KEY,
	nombre VARCHAR(255) NOT NULL,
	fecha date
);

CREATE TABLE imagenes(
	id INT NOT NULL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	fecha date
);

CREATE TABLE documento_marca(
	id INT NOT NULL PRIMARY KEY,
	nombre VARCHAR(255) NOT NULL,
	fecha date,
	id_doc int,
	CONSTRAINT fk_doc_docMarca FOREIGN KEY (id_doc) REFERENCES documento (id)
);

CREATE TABLE marca(
	id INT NOT NULL PRIMARY KEY,
	nombre VARCHAR(255) NOT NULL,
	fecha date,
	id_doc int,
	id_alias int,
	CONSTRAINT fk_Marca_doc FOREIGN KEY (id_doc) REFERENCES documento_marca (id),
	CONSTRAINT fk_alias_marca FOREIGN KEY (id_alias) REFERENCES alias (id)
);

CREATE TABLE resultado(
	id INT NOT NULL PRIMARY KEY,
	fecha date,
	id_usuario int,
	id_img int,
	CONSTRAINT fk_img_result FOREIGN KEY (id_img) REFERENCES imagenes (id),
	CONSTRAINT fk_user_result FOREIGN KEY (id_usuario) REFERENCES usuario (id)
);