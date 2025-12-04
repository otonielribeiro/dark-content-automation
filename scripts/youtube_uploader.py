#!/usr/bin/env python3
"""
Upload Automatizado para YouTube Shorts
Usa YouTube Data API v3
"""

import os
import json
from pathlib import Path
from datetime import datetime

# Nota: Este script requer autenticação OAuth2 do Google
# Para uso completo, você precisará configurar credenciais no Google Cloud Console

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"

class YouTubeUploader:
    """Faz upload de vídeos para YouTube Shorts"""
    
    def __init__(self):
        """
        Inicializa uploader do YouTube
        
        IMPORTANTE: Para usar este script, você precisa:
        1. Criar projeto no Google Cloud Console
        2. Ativar YouTube Data API v3
        3. Criar credenciais OAuth 2.0
        4. Baixar client_secrets.json
        5. Instalar: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
        """
        self.credentials_file = BASE_DIR / "credentials" / "youtube_client_secrets.json"
        self.token_file = BASE_DIR / "credentials" / "youtube_token.json"
        
    def authenticate(self):
        """Autentica com YouTube API"""
        try:
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from google.auth.transport.requests import Request
            from googleapiclient.discovery import build
            
            SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
            
            creds = None
            
            # Carrega token salvo se existir
            if self.token_file.exists():
                creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)
            
            # Se não há credenciais válidas, faz login
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not self.credentials_file.exists():
                        raise Exception(
                            "Arquivo de credenciais não encontrado!\n"
                            "Baixe client_secrets.json do Google Cloud Console e salve em:\n"
                            f"{self.credentials_file}"
                        )
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_file), SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Salva token
                self.token_file.parent.mkdir(exist_ok=True)
                with open(self.token_file, 'w') as token:
                    token.write(creds.to_json())
            
            # Cria serviço YouTube
            self.youtube = build('youtube', 'v3', credentials=creds)
            return True
            
        except ImportError:
            print("❌ Bibliotecas do Google não instaladas!")
            print("Instale com: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
            return False
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return False
    
    def upload_video(self, video_file, title, description, tags=None, 
                    category_id="22", privacy_status="public"):
        """
        Faz upload de vídeo para YouTube
        
        Args:
            video_file: Path do arquivo de vídeo
            title: Título do vídeo
            description: Descrição
            tags: Lista de tags
            category_id: ID da categoria (22 = People & Blogs)
            privacy_status: public, private ou unlisted
        
        Returns:
            ID do vídeo no YouTube
        """
        
        from googleapiclient.http import MediaFileUpload
        
        # Prepara metadados
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Prepara upload
        media = MediaFileUpload(
            str(video_file),
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        # Faz upload
        request = self.youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        print(f"📤 Fazendo upload para YouTube...")
        response = request.execute()
        
        video_id = response['id']
        video_url = f"https://youtube.com/shorts/{video_id}"
        
        print(f"✅ Upload concluído!")
        print(f"   ID: {video_id}")
        print(f"   URL: {video_url}")
        
        return video_id, video_url
    
    def upload_from_package(self, package_file, privacy_status="private"):
        """
        Faz upload a partir de um pacote de conteúdo
        
        Args:
            package_file: Arquivo JSON do pacote
            privacy_status: Status de privacidade (recomendado: private para revisão)
        """
        
        # Carrega pacote
        with open(package_file, 'r', encoding='utf-8') as f:
            package = json.load(f)
        
        video_file = package.get('video_file')
        if not video_file or not Path(video_file).exists():
            raise Exception("Vídeo não encontrado! Compile o vídeo primeiro.")
        
        # Prepara metadados
        metadata = package['metadata']
        title = metadata.get('titulo', package['caso_titulo'])
        description = metadata.get('descricao', '')
        hashtags = metadata.get('hashtags', '')
        
        # Adiciona hashtags à descrição
        full_description = f"{description}\n\n{hashtags}\n\n#Shorts #CasosPoliciais #TrueCrime"
        
        # Extrai tags
        tags = [tag.strip('#') for tag in hashtags.split() if tag.startswith('#')]
        tags.extend(['shorts', 'casos policiais', 'true crime', 'documentário'])
        
        # Autentica
        if not self.authenticate():
            print("⚠️ Não foi possível autenticar. Configure as credenciais primeiro.")
            return None
        
        # Faz upload
        print(f"🎬 Fazendo upload: {title}")
        video_id, video_url = self.upload_video(
            video_file=video_file,
            title=title[:100],  # YouTube limita a 100 caracteres
            description=full_description[:5000],  # Limite de 5000 caracteres
            tags=tags[:500],  # Limite de 500 caracteres total
            privacy_status=privacy_status
        )
        
        # Atualiza pacote
        package['youtube_video_id'] = video_id
        package['youtube_url'] = video_url
        package['youtube_upload_date'] = datetime.now().isoformat()
        package['status'] = 'publicado_youtube'
        
        with open(package_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, ensure_ascii=False, indent=2)
        
        return video_id, video_url


# Exemplo de uso
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("YOUTUBE SHORTS UPLOADER")
    print("=" * 60)
    print()
    print("⚠️  CONFIGURAÇÃO NECESSÁRIA:")
    print("1. Acesse: https://console.cloud.google.com")
    print("2. Crie um projeto")
    print("3. Ative 'YouTube Data API v3'")
    print("4. Crie credenciais OAuth 2.0")
    print("5. Baixe o arquivo JSON de credenciais")
    print("6. Salve como: credentials/youtube_client_secrets.json")
    print()
    
    if len(sys.argv) > 1:
        package_file = sys.argv[1]
        uploader = YouTubeUploader()
        
        # Upload como privado por padrão (para revisão)
        uploader.upload_from_package(package_file, privacy_status="private")
    else:
        print("Uso: python youtube_uploader.py <arquivo_pacote.json>")
