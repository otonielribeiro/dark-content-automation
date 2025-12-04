#!/usr/bin/env python3
"""
Gerador de Narração com ElevenLabs
Converte roteiro em áudio de narração profissional
"""

import os
import json
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"

class VoiceGenerator:
    """Gera narração usando ElevenLabs API"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY não configurada!")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Vozes recomendadas para conteúdo dark em português
        self.recommended_voices = {
            "masculina_grave": "21m00Tcm4TlvDq8ikWAM",  # Rachel (adaptável)
            "feminina_suave": "EXAVITQu4vr4xnSDxMaL",   # Bella (suave)
            "masculina_seria": "VR6AewLTigWG4xSOukaG"   # Arnold (séria)
        }
    
    def list_available_voices(self):
        """Lista vozes disponíveis na conta"""
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['voices']
        else:
            raise Exception(f"Erro ao listar vozes: {response.text}")
    
    def generate_audio(self, text, voice_id=None, output_filename=None):
        """
        Gera áudio a partir do texto
        
        Args:
            text: Texto do roteiro
            voice_id: ID da voz (usa padrão se não especificado)
            output_filename: Nome do arquivo de saída
        
        Returns:
            Path do arquivo de áudio gerado
        """
        
        # Usa voz padrão se não especificada
        if not voice_id:
            voice_id = self.recommended_voices["feminina_suave"]
        
        # URL da API
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        # Headers
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        # Configurações de voz otimizadas para narração dark
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",  # Melhor para português
            "voice_settings": {
                "stability": 0.6,        # Estabilidade moderada
                "similarity_boost": 0.8,  # Alta similaridade
                "style": 0.5,            # Estilo moderado
                "use_speaker_boost": True
            }
        }
        
        # Faz requisição
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Define nome do arquivo
            if not output_filename:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"narration_{timestamp}.mp3"
            
            # Salva arquivo
            output_path = OUTPUT_DIR / output_filename
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Áudio gerado: {output_path}")
            return output_path
        else:
            raise Exception(f"Erro ao gerar áudio: {response.status_code} - {response.text}")
    
    def generate_from_content_package(self, package_file):
        """Gera áudio a partir de um pacote de conteúdo"""
        
        # Carrega pacote
        with open(package_file, 'r', encoding='utf-8') as f:
            package = json.load(f)
        
        script = package['script']
        timestamp = package['timestamp']
        
        # Gera áudio
        print(f"🎙️ Gerando narração para: {package['caso_titulo']}")
        audio_file = self.generate_audio(
            text=script,
            output_filename=f"narration_{timestamp}.mp3"
        )
        
        # Atualiza pacote
        package['audio_file'] = str(audio_file)
        package['status'] = 'audio_gerado'
        
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, ensure_ascii=False, indent=2)
        
        return audio_file


# Exemplo de uso standalone
if __name__ == "__main__":
    import sys
    
    # Verifica se foi passado arquivo de pacote
    if len(sys.argv) > 1:
        package_file = sys.argv[1]
        generator = VoiceGenerator()
        generator.generate_from_content_package(package_file)
    else:
        # Teste simples
        print("⚠️ Modo de teste - configure ELEVENLABS_API_KEY primeiro!")
        print("\nPara usar: python voice_generator.py <arquivo_pacote.json>")
        print("\nOu configure a API key:")
        print("export ELEVENLABS_API_KEY='sua_chave_aqui'")
