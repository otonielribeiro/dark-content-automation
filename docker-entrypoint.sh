#!/bin/bash
set -e

echo "========================================="
echo "Dark Content Automation - Starting..."
echo "========================================="

# Verifica variáveis de ambiente obrigatórias
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "⚠️  WARNING: ELEVENLABS_API_KEY não configurada!"
    echo "   Configure com: -e ELEVENLABS_API_KEY=sua_chave"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY não configurada!"
    echo "   Configure com: -e OPENAI_API_KEY=sua_chave"
fi

# Executa comando passado
exec "$@"
