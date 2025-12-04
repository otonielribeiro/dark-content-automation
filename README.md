# Sistema de Automação de Conteúdo Dark para TikTok e YouTube

**Autor**: Manus AI
**Versão**: 1.0
**Data**: 03/12/2025

## 1. Visão Geral

Este projeto é um sistema completo para automatizar a criação e publicação de vídeos curtos (Shorts/TikTok) sobre casos policiais reais. O sistema gera roteiros, narrações, compila os vídeos e os prepara para publicação, com o objetivo de postar um novo vídeo a cada 2 dias.

O conteúdo é inspirado no estilo "dark content" de canais como "Life Laps", utilizando uma estética cinematográfica, narração séria e temas de mistério.

## 2. Arquitetura e Fluxo de Trabalho

O sistema é modular e segue o seguinte fluxo:

1.  **Seleção do Caso**: Um caso policial é selecionado aleatoriamente do banco de dados (`data/casos_policiais.json`).
2.  **Geração de Roteiro**: A API do OpenRouter (GPT-4o-mini) cria um roteiro cinematográfico para o caso.
3.  **Geração de Narração**: A API da ElevenLabs converte o roteiro em um áudio de narração com voz natural.
4.  **Compilação do Vídeo**: O FFmpeg combina um fundo animado, a narração, uma música de fundo (opcional) e o título para criar o vídeo final no formato 9:16.
5.  **Upload (Opcional)**: O vídeo é enviado para o YouTube como "Privado" para revisão, utilizando a API do YouTube.

## 3. Estrutura de Diretórios

```
/dark_content_automation
├── 📂 assets/              # Músicas de fundo, fontes, etc.
│   └── background_music.mp3 (opcional)
├── 📂 credentials/          # Arquivos de credenciais (NÃO COMPARTILHAR)
│   └── youtube_client_secrets.json (a ser criado)
├── 📂 data/                 # Banco de dados e controle
│   ├── casos_policiais.json # Lista de casos
│   └── casos_usados.json    # Controle de casos já postados
├── 📂 logs/                 # Logs de execução
├── 📂 output/               # Arquivos gerados (pacotes, áudios, vídeos)
├── 📂 scripts/              # Scripts Python do sistema
│   ├── automation_pipeline.py
│   ├── content_generator.py
│   ├── scheduler.py
│   ├── video_compiler.py
│   ├── voice_generator.py
│   └── youtube_uploader.py
├── 📜 README.md              # Este guia
└── 📜 run_scheduler.py       # Exemplo de agendador simples
```

## 4. Configuração Obrigatória

Antes de executar o sistema, você precisa configurar as chaves de API e credenciais.

### 4.1. Chave do OpenRouter

O sistema usa o **OpenRouter** para acessar modelos de IA com preços competitivos.

1.  Acesse [openrouter.ai/keys](https://openrouter.ai/keys) e crie uma conta.
2.  Gere uma nova API key.
3.  No terminal, configure a chave como uma variável de ambiente:

    ```bash
    export OPENROUTER_API_KEY='sk-or-v1-sua_chave_aqui'
    ```

    **Importante**: Você precisa executar este comando toda vez que iniciar uma nova sessão de terminal, ou adicioná-lo ao seu arquivo `~/.bashrc` para torná-lo permanente.

### 4.2. Chave da ElevenLabs

1.  Crie uma conta em [elevenlabs.io](https://elevenlabs.io).
2.  Vá para o seu perfil e encontre sua **API Key**.
3.  No terminal, configure a chave como uma variável de ambiente:

    ```bash
    export ELEVENLABS_API_KEY=\'sua_chave_de_api_aqui\'
    ```

    **Importante**: Você precisa executar este comando toda vez que iniciar uma nova sessão de terminal, ou adicioná-lo ao seu arquivo `~/.bashrc` para torná-lo permanente.

### 4.3. Credenciais da API do YouTube (para Upload Automático)

Esta é a etapa mais complexa e é **opcional**. Se não for configurada, o sistema irá gerar os vídeos e você poderá fazer o upload manualmente.

1.  **Google Cloud Console**: Acesse [console.cloud.google.com](https://console.cloud.google.com).
2.  **Crie um Novo Projeto**.
3.  No menu de busca, procure e ative a **"YouTube Data API v3"**.
4.  Vá para "Credenciais", clique em "Criar Credenciais" e selecione **"ID do cliente OAuth"**.
5.  Selecione **"Aplicativo para computador"** como tipo de aplicativo.
6.  Após a criação, clique no botão de download (ícone de seta para baixo) para baixar o arquivo JSON. **Renomeie este arquivo para `youtube_client_secrets.json`**.
7.  Mova o arquivo para o diretório `credentials/`.

Na primeira vez que o script de upload for executado, ele abrirá uma janela no seu navegador pedindo autorização. Após conceder permissão, um arquivo `youtube_token.json` será criado, e a autenticação será automática nas próximas vezes.

## 5. Como Usar o Sistema

### 5.1. Execução Manual (Recomendado para Testes)

Você pode executar o pipeline completo com um único comando. Isso irá gerar um vídeo do zero e salvá-lo no diretório `output/`.

```bash
# Navegue até o diretório do projeto
cd /home/ubuntu/dark_content_automation

# Execute o pipeline principal
python3 scripts/automation_pipeline.py
```

O vídeo final e o pacote de conteúdo (JSON com roteiro, metadados, etc.) estarão na pasta `output/`.

### 5.2. Execução com Upload Automático

Se você configurou as credenciais do YouTube, pode usar a flag `--auto-upload`.

```bash
python3 scripts/automation_pipeline.py --auto-upload
```

O vídeo será enviado para o seu canal do YouTube como **privado**, para que você possa revisá-lo antes de publicar.

## 6. Agendamento Automático

Para fazer uma postagem a cada 2 dias, você precisa agendar a execução do `automation_pipeline.py`. O método mais simples é usar o `run_scheduler.py`.

### Agendador Simples (Recomendado)

Este método não requer configurações complexas no sistema operacional.

1.  **Inicie o agendador em background**:

    ```bash
    cd /home/ubuntu/dark_content_automation

    nohup python3 run_scheduler.py > scheduler.log 2>&1 &
    ```

    Isso iniciará o processo em segundo plano. Ele executará o pipeline imediatamente e, depois, a cada 2 dias. O progresso será salvo no arquivo `scheduler.log`.

2.  **Para parar o agendador**:

    ```bash
    pkill -f run_scheduler.py
    ```

## 7. Customização

### 7.1. Adicionar Novos Casos

Edite o arquivo `data/casos_policiais.json` e adicione novos objetos JSON com a seguinte estrutura:

```json
{
  "id": 26, // Use um ID único
  "titulo": "O Nome do Novo Caso",
  "resumo": "Um resumo breve e impactante do caso.",
  "data": "Data do ocorrido",
  "local": "Local do ocorrido",
  "categoria": "categoria_do_crime"
}
```

### 7.2. Mudar a Voz da Narração

Edite o arquivo `scripts/voice_generator.py`. Na função `__init__`, você pode alterar o ID da voz padrão ou adicionar novas vozes da sua conta ElevenLabs.

```python
# Em voice_generator.py
self.recommended_voices = {
    "masculina_grave": "21m00Tcm4TlvDq8ikWAM",
    "feminina_suave": "EXAVITQu4vr4xnSDxMaL",
    "masculina_seria": "VR6AewLTigWG4xSOukaG"
}

# Altere a voz padrão na função generate_audio
if not voice_id:
    voice_id = self.recommended_voices["masculina_grave"] # Mude aqui
```

### 7.3. Adicionar Música de Fundo

Coloque um arquivo de áudio (ex: `background_music.mp3`) no diretório `assets/`. O `video_compiler.py` irá detectá-lo e adicioná-lo automaticamente aos vídeos com um volume baixo.
