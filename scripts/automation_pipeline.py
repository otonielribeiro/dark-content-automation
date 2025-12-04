#!/usr/bin/env python3
"""
Pipeline de Automação Completo
Executa todo o fluxo: geração → narração → vídeo → upload
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Adiciona diretório de scripts ao path
sys.path.insert(0, str(Path(__file__).parent))

from content_generator import ContentGenerator
from voice_generator import VoiceGenerator
from video_compiler import VideoCompiler
from youtube_uploader import YouTubeUploader

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

class AutomationPipeline:
    """Pipeline completo de automação de conteúdo"""
    
    def __init__(self, auto_upload=False):
        """
        Inicializa pipeline
        
        Args:
            auto_upload: Se True, faz upload automático (requer configuração)
        """
        self.auto_upload = auto_upload
        self.log_file = LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Cria diretórios necessários
        OUTPUT_DIR.mkdir(exist_ok=True)
        LOGS_DIR.mkdir(exist_ok=True)
    
    def log(self, message):
        """Registra mensagem no log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def run_full_pipeline(self):
        """
        Executa pipeline completo
        
        Returns:
            Dicionário com resultados
        """
        
        self.log("=" * 70)
        self.log("🚀 INICIANDO PIPELINE DE AUTOMAÇÃO")
        self.log("=" * 70)
        
        try:
            # ETAPA 1: Geração de Conteúdo
            self.log("\n📝 ETAPA 1/5: Geração de Conteúdo")
            self.log("-" * 70)
            
            generator = ContentGenerator()
            package_file = generator.generate_complete_content()
            
            self.log(f"✅ Pacote de conteúdo criado: {package_file}")
            
            # Carrega pacote
            with open(package_file, 'r', encoding='utf-8') as f:
                package = json.load(f)
            
            # ETAPA 2: Geração de Narração
            self.log("\n🎙️ ETAPA 2/5: Geração de Narração")
            self.log("-" * 70)
            
            # Verifica se API key está configurada
            if not os.getenv("ELEVENLABS_API_KEY"):
                self.log("⚠️ ELEVENLABS_API_KEY não configurada!")
                self.log("   Configure com: export ELEVENLABS_API_KEY='sua_chave'")
                self.log("   Pulando geração de narração...")
                audio_file = None
            else:
                voice_gen = VoiceGenerator()
                audio_file = voice_gen.generate_from_content_package(package_file)
                self.log(f"✅ Narração gerada: {audio_file}")
            
            # ETAPA 3: Compilação de Vídeo
            self.log("\n🎬 ETAPA 3/5: Compilação de Vídeo")
            self.log("-" * 70)
            
            if audio_file:
                compiler = VideoCompiler()
                video_file = compiler.compile_video_from_package(package_file)
                self.log(f"✅ Vídeo compilado: {video_file}")
            else:
                self.log("⚠️ Pulando compilação (sem narração)")
                video_file = None
            
            # ETAPA 4: Upload para YouTube (opcional)
            self.log("\n📤 ETAPA 4/5: Upload para YouTube")
            self.log("-" * 70)
            
            youtube_url = None
            if self.auto_upload and video_file:
                try:
                    uploader = YouTubeUploader()
                    video_id, youtube_url = uploader.upload_from_package(
                        package_file, 
                        privacy_status="private"  # Privado para revisão
                    )
                    self.log(f"✅ Upload concluído: {youtube_url}")
                except Exception as e:
                    self.log(f"⚠️ Erro no upload: {e}")
                    self.log("   Vídeo salvo localmente para upload manual")
            else:
                self.log("⏭️ Upload automático desabilitado")
                self.log(f"   Vídeo disponível em: {video_file}")
            
            # ETAPA 5: Preparação para TikTok
            self.log("\n📱 ETAPA 5/5: Preparação para TikTok")
            self.log("-" * 70)
            self.log("⚠️ TikTok não possui API oficial pública")
            self.log("   Opções para upload:")
            self.log("   1. Upload manual pelo app TikTok")
            self.log("   2. Usar ferramentas de terceiros (Publer, Buffer)")
            self.log("   3. Bibliotecas não-oficiais (risco de bloqueio)")
            self.log(f"\n   Vídeo pronto: {video_file}")
            
            # Resumo Final
            self.log("\n" + "=" * 70)
            self.log("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
            self.log("=" * 70)
            
            # Carrega pacote atualizado
            with open(package_file, 'r', encoding='utf-8') as f:
                final_package = json.load(f)
            
            self.log(f"\n📊 RESUMO:")
            self.log(f"   Caso: {final_package['caso_titulo']}")
            self.log(f"   Título: {final_package['metadata'].get('titulo', 'N/A')}")
            self.log(f"   Hashtags: {final_package['metadata'].get('hashtags', 'N/A')}")
            if audio_file:
                self.log(f"   Áudio: {audio_file}")
            if video_file:
                self.log(f"   Vídeo: {video_file}")
            if youtube_url:
                self.log(f"   YouTube: {youtube_url}")
            
            self.log(f"\n📁 Pacote completo: {package_file}")
            
            return {
                'success': True,
                'package_file': str(package_file),
                'audio_file': str(audio_file) if audio_file else None,
                'video_file': str(video_file) if video_file else None,
                'youtube_url': youtube_url,
                'metadata': final_package['metadata']
            }
            
        except Exception as e:
            self.log(f"\n❌ ERRO NO PIPELINE: {e}")
            import traceback
            self.log(traceback.format_exc())
            
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Função principal"""
    
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Pipeline de Automação de Conteúdo Dark'
    )
    parser.add_argument(
        '--auto-upload',
        action='store_true',
        help='Ativa upload automático para YouTube (requer configuração)'
    )
    
    args = parser.parse_args()
    
    # Executa pipeline
    pipeline = AutomationPipeline(auto_upload=args.auto_upload)
    result = pipeline.run_full_pipeline()
    
    # Retorna código de saída
    sys.exit(0 if result['success'] else 1)


if __name__ == "__main__":
    main()
