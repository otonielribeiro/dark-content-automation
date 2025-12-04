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

if [ -z "$OPENROUTER_API_KEY" ]; then
    echo "⚠️  WARNING: OPENROUTER_API_KEY não configurada!"
    echo "   Configure com: -e OPENROUTER_API_KEY=sk-or-v1-..."
fi

# Executa comando passado
exec "$@"
