CREATE DATABASE IF NOT EXISTS tech_dashboard
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tech_dashboard;

-- Supervisores
CREATE TABLE IF NOT EXISTS supervisores (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    senha         VARCHAR(255) NOT NULL,   
    criado_em     DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- técnicos de Atendimento
CREATE TABLE IF NOT EXISTS tecnicos (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    senha           VARCHAR(255) NOT NULL, 
    status          ENUM('disponivel', 'em_atendimento') NOT NULL DEFAULT 'disponivel',
    qtd_chamados    INT NOT NULL DEFAULT 0,
    criado_em       DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em   DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Dados de exemplo para desenvolvimento

INSERT INTO supervisores (name, senha) VALUES
    ('Marcos', '2564');

INSERT INTO tecnicos (name, senha, status, qtd_chamados) VALUES
    ('Davi',          '1234', 'disponivel',     2),
    ('Maria Souza',   '1234', 'em_atendimento', 5),
    ('Pedro Alves',   '1234', 'disponivel',     0),
    ('Ana Lima',      '1234', 'em_atendimento', 3);