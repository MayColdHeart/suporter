# Usa uma imagem oficial do Python leve
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia apenas o requirements primeiro para otimizar o cache
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do projeto (o .dockerignore vai barrar o .env)
COPY . .

# ... (mantenha todo o resto igual em cima)

# Expõe a porta do Flask
EXPOSE 5000

# Comando duplo: Roda o setup do banco PRIMEIRO, se der certo, roda o Flask
CMD ["sh", "-c", "python setup_db.py && python app.py"]