#!/usr/bin/env python3
"""
Agendador de Execução Automática
Configura execução do pipeline a cada 2 dias
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent.parent

class Scheduler:
    """Gerencia agendamento de execução automática"""
    
    def __init__(self):
        self.pipeline_script = BASE_DIR / "scripts" / "automation_pipeline.py"
        self.log_dir = BASE_DIR / "logs"
    
    def create_cron_job(self, interval_days=2, hour=10, minute=0):
        """
        Cria job no crontab para execução automática
        
        Args:
            interval_days: Intervalo em dias (2 = a cada 2 dias)
            hour: Hora da execução (0-23)
            minute: Minuto da execução (0-59)
        """
        
        # Comando para executar
        python_path = sys.executable
        script_path = self.pipeline_script
        log_file = self.log_dir / "cron_output.log"
        
        # Cron expression para a cada N dias às HH:MM
        # Como cron não suporta "a cada N dias" diretamente, 
        # usamos uma abordagem com script wrapper
        
        cron_command = (
            f"{minute} {hour} */{interval_days} * * "
            f"cd {BASE_DIR} && {python_path} {script_path} "
            f">> {log_file} 2>&1"
        )
        
        print("=" * 70)
        print("CONFIGURAÇÃO DE AGENDAMENTO AUTOMÁTICO")
        print("=" * 70)
        print()
        print(f"📅 Frequência: A cada {interval_days} dias")
        print(f"🕐 Horário: {hour:02d}:{minute:02d}")
        print()
        print("Para adicionar ao crontab, execute:")
        print()
        print("1. Abra o crontab:")
        print("   crontab -e")
        print()
        print("2. Adicione esta linha:")
        print()
        print(f"   {cron_command}")
        print()
        print("3. Salve e feche o editor")
        print()
        print("=" * 70)
        print()
        
        # Salva comando em arquivo para referência
        cron_file = BASE_DIR / "cron_command.txt"
        with open(cron_file, 'w') as f:
            f.write("# Comando para adicionar ao crontab\n")
            f.write("# Execute: crontab -e\n")
            f.write("# Adicione a linha abaixo:\n\n")
            f.write(cron_command + "\n")
        
        print(f"💾 Comando salvo em: {cron_file}")
        print()
        
        return cron_command
    
    def create_systemd_timer(self, interval_days=2):
        """
        Cria timer do systemd (alternativa ao cron)
        Mais confiável para tarefas periódicas
        """
        
        service_name = "dark-content-automation"
        
        # Arquivo .service
        service_content = f"""[Unit]
Description=Dark Content Automation Pipeline
After=network.target

[Service]
Type=oneshot
User={os.getenv('USER', 'ubuntu')}
WorkingDirectory={BASE_DIR}
ExecStart={sys.executable} {self.pipeline_script}
StandardOutput=append:{self.log_dir}/systemd_output.log
StandardError=append:{self.log_dir}/systemd_error.log

[Install]
WantedBy=multi-user.target
"""
        
        # Arquivo .timer
        timer_content = f"""[Unit]
Description=Dark Content Automation Timer
Requires={service_name}.service

[Timer]
OnCalendar=*-*-* 10:00:00
Persistent=true

[Install]
WantedBy=timers.target
"""
        
        service_file = BASE_DIR / f"{service_name}.service"
        timer_file = BASE_DIR / f"{service_name}.timer"
        
        with open(service_file, 'w') as f:
            f.write(service_content)
        
        with open(timer_file, 'w') as f:
            f.write(timer_content)
        
        print("=" * 70)
        print("CONFIGURAÇÃO DE SYSTEMD TIMER (RECOMENDADO)")
        print("=" * 70)
        print()
        print("Arquivos criados:")
        print(f"  - {service_file}")
        print(f"  - {timer_file}")
        print()
        print("Para instalar:")
        print()
        print("1. Copie os arquivos para /etc/systemd/system/:")
        print(f"   sudo cp {service_file} /etc/systemd/system/")
        print(f"   sudo cp {timer_file} /etc/systemd/system/")
        print()
        print("2. Recarregue o systemd:")
        print("   sudo systemctl daemon-reload")
        print()
        print("3. Ative e inicie o timer:")
        print(f"   sudo systemctl enable {service_name}.timer")
        print(f"   sudo systemctl start {service_name}.timer")
        print()
        print("4. Verifique o status:")
        print(f"   sudo systemctl status {service_name}.timer")
        print()
        print("=" * 70)
        print()
    
    def create_simple_scheduler(self, interval_days=2):
        """
        Cria script Python simples com loop de agendamento
        Alternativa mais simples que não requer configuração do sistema
        """
        
        scheduler_script = BASE_DIR / "run_scheduler.py"
        
        content = f"""#!/usr/bin/env python3
\"\"\"
Agendador Simples - Executa pipeline a cada {interval_days} dias
Mantenha este script rodando em background
\"\"\"

import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

PIPELINE_SCRIPT = Path(__file__).parent / "scripts" / "automation_pipeline.py"
INTERVAL_DAYS = {interval_days}
INTERVAL_SECONDS = INTERVAL_DAYS * 24 * 60 * 60

def run_pipeline():
    \"\"\"Executa o pipeline\"\"\"
    print(f"[{{datetime.now()}}] Executando pipeline...")
    
    try:
        result = subprocess.run(
            ['python3', str(PIPELINE_SCRIPT)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"[{{datetime.now()}}] ✅ Pipeline concluído com sucesso!")
        else:
            print(f"[{{datetime.now()}}] ❌ Pipeline falhou!")
            print(result.stderr)
    
    except Exception as e:
        print(f"[{{datetime.now()}}] ❌ Erro: {{e}}")

def main():
    print("=" * 70)
    print("AGENDADOR AUTOMÁTICO INICIADO")
    print("=" * 70)
    print(f"Intervalo: A cada {{INTERVAL_DAYS}} dias")
    print(f"Próxima execução: {{datetime.now() + timedelta(seconds=INTERVAL_SECONDS)}}")
    print()
    print("Pressione Ctrl+C para parar")
    print("=" * 70)
    print()
    
    try:
        while True:
            run_pipeline()
            
            next_run = datetime.now() + timedelta(seconds=INTERVAL_SECONDS)
            print(f"\\n[{{datetime.now()}}] Próxima execução: {{next_run}}")
            print(f"Aguardando {{INTERVAL_DAYS}} dias...")
            
            time.sleep(INTERVAL_SECONDS)
    
    except KeyboardInterrupt:
        print("\\n\\nAgendador interrompido pelo usuário.")

if __name__ == "__main__":
    main()
"""
        
        with open(scheduler_script, 'w') as f:
            f.write(content)
        
        # Torna executável
        scheduler_script.chmod(0o755)
        
        print("=" * 70)
        print("AGENDADOR SIMPLES CRIADO")
        print("=" * 70)
        print()
        print(f"📄 Script: {scheduler_script}")
        print()
        print("Para executar:")
        print()
        print("1. Em foreground (para testes):")
        print(f"   python3 {scheduler_script}")
        print()
        print("2. Em background (produção):")
        print(f"   nohup python3 {scheduler_script} > scheduler.log 2>&1 &")
        print()
        print("3. Para parar:")
        print("   pkill -f run_scheduler.py")
        print()
        print("=" * 70)
        print()
        
        return scheduler_script


def main():
    """Função principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Configurador de Agendamento Automático'
    )
    parser.add_argument(
        '--method',
        choices=['cron', 'systemd', 'simple'],
        default='simple',
        help='Método de agendamento (padrão: simple)'
    )
    parser.add_argument(
        '--interval',
        type=int,
        default=2,
        help='Intervalo em dias (padrão: 2)'
    )
    
    args = parser.parse_args()
    
    scheduler = Scheduler()
    
    if args.method == 'cron':
        scheduler.create_cron_job(interval_days=args.interval)
    elif args.method == 'systemd':
        scheduler.create_systemd_timer(interval_days=args.interval)
    else:
        scheduler.create_simple_scheduler(interval_days=args.interval)


if __name__ == "__main__":
    main()
