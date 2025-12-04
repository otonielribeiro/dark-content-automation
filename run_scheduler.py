#!/usr/bin/env python3
"""
Agendador Simples - Executa pipeline a cada 2 dias
Mantenha este script rodando em background
"""

import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

PIPELINE_SCRIPT = Path(__file__).parent / "scripts" / "automation_pipeline.py"
INTERVAL_DAYS = 2
INTERVAL_SECONDS = INTERVAL_DAYS * 24 * 60 * 60

def run_pipeline():
    """Executa o pipeline"""
    print(f"[{datetime.now()}] Executando pipeline...")
    
    try:
        result = subprocess.run(
            ['python3', str(PIPELINE_SCRIPT)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] ✅ Pipeline concluído com sucesso!")
        else:
            print(f"[{datetime.now()}] ❌ Pipeline falhou!")
            print(result.stderr)
    
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erro: {e}")

def main():
    print("=" * 70)
    print("AGENDADOR AUTOMÁTICO INICIADO")
    print("=" * 70)
    print(f"Intervalo: A cada {INTERVAL_DAYS} dias")
    print(f"Próxima execução: {datetime.now() + timedelta(seconds=INTERVAL_SECONDS)}")
    print()
    print("Pressione Ctrl+C para parar")
    print("=" * 70)
    print()
    
    try:
        while True:
            run_pipeline()
            
            next_run = datetime.now() + timedelta(seconds=INTERVAL_SECONDS)
            print(f"\n[{datetime.now()}] Próxima execução: {next_run}")
            print(f"Aguardando {INTERVAL_DAYS} dias...")
            
            time.sleep(INTERVAL_SECONDS)
    
    except KeyboardInterrupt:
        print("\n\nAgendador interrompido pelo usuário.")

if __name__ == "__main__":
    main()
