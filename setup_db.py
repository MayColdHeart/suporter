"""
setup_db.py
-----------
Cria o banco de dados e as tabelas necessárias para o Suporter.
"""

import sys
import time
import pymysql
from dotenv import load_dotenv
from config import Config

load_dotenv()
cfg = Config()

SCHEMA = """
CREATE TABLE IF NOT EXISTS supervisores (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    senha VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS tecnicos (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100) NOT NULL,
    senha        VARCHAR(255) NOT NULL,
    status       ENUM('disponivel', 'em_atendimento') NOT NULL DEFAULT 'disponivel',
    qtd_chamados INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

SEED = """
INSERT IGNORE INTO supervisores (id, name, senha) VALUES
    (1, 'Admin', 'admin123');

INSERT IGNORE INTO tecnicos (id, name, senha, status, qtd_chamados) VALUES
    (1, 'Técnico 01', 'tec123', 'disponivel', 0),
    (2, 'Técnico 02', 'tec123', 'disponivel', 0);
"""

def run():
    print(f"Tentando conectar em {cfg.MARIADB_HOST}:{cfg.MARIADB_PORT} como '{cfg.MARIADB_USER}'...")

    # Tenta conectar por até 15 segundos (5 tentativas x 3 segundos)
    max_tentativas = 5
    conn = None
    
    for tentativa in range(max_tentativas):
        try:
            conn = pymysql.connect(
                host=cfg.MARIADB_HOST,
                port=cfg.MARIADB_PORT,
                user=cfg.MARIADB_USER,
                password=cfg.MARIADB_PASSWORD,
                charset="utf8mb4",
                autocommit=True,
            )
            print("Conexão com o banco estabelecida com sucesso!")
            break
        except pymysql.err.OperationalError as e:
            print(f"Aguardando banco de dados iniciar... (Tentativa {tentativa + 1}/{max_tentativas})")
            time.sleep(3)
            
    if not conn:
        print("\nERRO FATAL: Não foi possível conectar ao banco de dados após várias tentativas.")
        sys.exit(1)

    with conn.cursor() as cur:
        # Cria o banco se não existir
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{cfg.MARIADB_DB}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        print(f"Banco '{cfg.MARIADB_DB}' pronto.")

        cur.execute(f"USE `{cfg.MARIADB_DB}`")

        # Cria tabelas
        for statement in SCHEMA.strip().split(";"):
            statement = statement.strip()
            if statement:
                cur.execute(statement)
        print("Tabelas criadas.")

        # Insere dados de exemplo
        for statement in SEED.strip().split(";"):
            statement = statement.strip()
            if statement:
                cur.execute(statement)
        print("Dados de exemplo inseridos.")

    conn.close()
    print("\nSetup concluido! Usuarios de teste:")
    print("  Supervisor -> ID: 1  | Senha: admin123")
    print("  Tecnico    -> ID: 1  | Senha: tec123")
    print("  Tecnico    -> ID: 2  | Senha: tec123")

if __name__ == "__main__":
    run()