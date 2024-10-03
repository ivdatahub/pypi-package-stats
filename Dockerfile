FROM python:3.9-slim

# Defina a variável de ambiente para não gerar bytecode compilado
ENV PYTHONDONTWRITEBYTECODE=1

# Defina a variável de ambiente para não armazenar buffer em stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# Instale as dependências do sistema e as ferramentas necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Instale pip, poetry e dependências
RUN pip install --upgrade pip \
    && pip install poetry

# Copie apenas os arquivos necessários para instalar as dependências
COPY pyproject.toml poetry.lock ./

# Instale as dependências usando Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# Copie o restante dos arquivos para o diretório de trabalho
COPY . .

# Entry point para o aplicativo
ENTRYPOINT ["python", "__main.py__"]