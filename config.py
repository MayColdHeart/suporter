import os
from dotenv import load_dotenv
 
load_dotenv()
 
 
class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-troque-em-producao")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
 
    # MariaDB
    MARIADB_HOST     = os.getenv("MARIADB_HOST", "localhost")
    MARIADB_PORT     = int(os.getenv("MARIADB_PORT", 3306))
    MARIADB_USER     = os.getenv("MARIADB_USER", "root")
    MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD", "891212")
    MARIADB_DB       = os.getenv("MARIADB_DB", "tech_dashboard")
    MARIADB_CHARSET  = "utf8mb4"