FROM python:3.11-slim

# Metadados
LABEL maintainer="otonielribeiro"
LABEL description="Sistema de Automação de Conteúdo Dark - Casos Policiais"

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Cria diretório de trabalho
WORKDIR /app

# Copia arquivos de requisitos
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código do projeto
COPY scripts/ ./scripts/
COPY data/ ./data/
COPY assets/ ./assets/
COPY .env.example .

# Cria diretórios necessários
RUN mkdir -p output logs credentials

# Define variáveis de ambiente padrão
ENV PYTHONUNBUFFERED=1

# Script de entrada
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python3", "scripts/automation_pipeline.py"]
