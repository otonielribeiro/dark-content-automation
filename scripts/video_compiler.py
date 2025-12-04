#!/usr/bin/env python3
"""
Compilador de Vídeo Automatizado
Cria vídeos finais com narração, música e legendas
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
ASSETS_DIR = BASE_DIR / "assets"

class VideoCompiler:
    """Compila vídeo final com todos os elementos"""
    
    def __init__(self):
        self.check_ffmpeg()
    
    def check_ffmpeg(self):
        """Verifica se FFmpeg está instalado"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            raise Exception("FFmpeg não está instalado! Instale com: sudo apt install ffmpeg")
    
    def create_background_video(self, duration, output_file):
        """
        Cria vídeo de fundo dark com movimento
        
        Args:
            duration: Duração em segundos
            output_file: Arquivo de saída
        """
        
        # Cria vídeo escuro com gradiente animado
        cmd = [
            'ffmpeg',
            '-f', 'lavfi',
            '-i', f'color=c=0x0a0a0a:s=1080x1920:d={duration}',  # Fundo preto vertical
            '-vf', 'noise=alls=20:allf=t+u',  # Adiciona ruído sutil
            '-c:v', 'libx264',
            '-t', str(duration),
            '-pix_fmt', 'yuv420p',
            '-y',
            str(output_file)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_file
    
    def add_audio_to_video(self, video_file, audio_file, output_file, 
                          background_music=None, music_volume=0.1):
        """
        Adiciona narração e música de fundo ao vídeo
        
        Args:
            video_file: Vídeo base
            audio_file: Narração
            output_file: Arquivo final
            background_music: Música de fundo (opcional)
            music_volume: Volume da música (0.0 a 1.0)
        """
        
        if background_music and Path(background_music).exists():
            # Com música de fundo
            cmd = [
                'ffmpeg',
                '-i', str(video_file),
                '-i', str(audio_file),
                '-i', str(background_music),
                '-filter_complex',
                f'[2:a]volume={music_volume}[music];[1:a][music]amix=inputs=2:duration=first[audio]',
                '-map', '0:v',
                '-map', '[audio]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                str(output_file)
            ]
        else:
            # Apenas narração
            cmd = [
                'ffmpeg',
                '-i', str(video_file),
                '-i', str(audio_file),
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-shortest',
                '-y',
                str(output_file)
            ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_file
    
    def add_text_overlay(self, video_file, text, output_file, 
                        position='center', fontsize=40, duration=None):
        """
        Adiciona texto/legenda ao vídeo
        
        Args:
            video_file: Vídeo de entrada
            text: Texto a adicionar
            output_file: Arquivo de saída
            position: Posição (top, center, bottom)
            fontsize: Tamanho da fonte
            duration: Duração do texto (None = todo o vídeo)
        """
        
        # Define posição vertical
        positions = {
            'top': 'h*0.15',
            'center': 'h*0.5',
            'bottom': 'h*0.85'
        }
        y_pos = positions.get(position, positions['center'])
        
        # Escapa caracteres especiais
        text = text.replace("'", "'\\\\\\''").replace(":", "\\:")
        
        # Filtro de texto
        text_filter = (
            f"drawtext=text='{text}':"
            f"fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
            f"fontsize={fontsize}:"
            f"fontcolor=white:"
            f"bordercolor=black:"
            f"borderw=2:"
            f"x=(w-text_w)/2:"
            f"y={y_pos}"
        )
        
        if duration:
            text_filter += f":enable='between(t,0,{duration})'"
        
        cmd = [
            'ffmpeg',
            '-i', str(video_file),
            '-vf', text_filter,
            '-c:a', 'copy',
            '-y',
            str(output_file)
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        return output_file
    
    def get_audio_duration(self, audio_file):
        """Obtém duração do arquivo de áudio"""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(audio_file)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    
    def compile_video_from_package(self, package_file):
        """
        Compila vídeo completo a partir de um pacote de conteúdo
        
        Args:
            package_file: Arquivo JSON do pacote
        
        Returns:
            Path do vídeo final
        """
        
        # Carrega pacote
        with open(package_file, 'r', encoding='utf-8') as f:
            package = json.load(f)
        
        timestamp = package['timestamp']
        audio_file = package.get('audio_file')
        
        if not audio_file or not Path(audio_file).exists():
            raise Exception("Arquivo de áudio não encontrado! Gere a narração primeiro.")
        
        print(f"🎬 Compilando vídeo: {package['caso_titulo']}")
        
        # 1. Obtém duração do áudio
        duration = self.get_audio_duration(audio_file)
        print(f"   Duração: {duration:.1f}s")
        
        # 2. Cria vídeo de fundo
        print("   Criando fundo...")
        bg_video = OUTPUT_DIR / f"bg_{timestamp}.mp4"
        self.create_background_video(duration, bg_video)
        
        # 3. Adiciona título no início (3 segundos)
        print("   Adicionando título...")
        title_video = OUTPUT_DIR / f"title_{timestamp}.mp4"
        title = package['metadata'].get('titulo', package['caso_titulo'])
        self.add_text_overlay(bg_video, title, title_video, 
                            position='center', fontsize=50, duration=3)
        
        # 4. Adiciona áudio (narração + música de fundo se disponível)
        print("   Adicionando áudio...")
        final_video = OUTPUT_DIR / f"final_{timestamp}.mp4"
        
        # Procura música de fundo
        bg_music = ASSETS_DIR / "background_music.mp3"
        if not bg_music.exists():
            bg_music = None
        
        self.add_audio_to_video(title_video, audio_file, final_video, 
                               background_music=bg_music, music_volume=0.08)
        
        # 5. Limpa arquivos temporários
        print("   Limpando arquivos temporários...")
        bg_video.unlink()
        title_video.unlink()
        
        # 6. Atualiza pacote
        package['video_file'] = str(final_video)
        package['status'] = 'video_compilado'
        
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Vídeo compilado: {final_video}")
        print(f"   Tamanho: {final_video.stat().st_size / 1024 / 1024:.1f} MB")
        
        return final_video


# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        package_file = sys.argv[1]
        compiler = VideoCompiler()
        compiler.compile_video_from_package(package_file)
    else:
        print("Uso: python video_compiler.py <arquivo_pacote.json>")
