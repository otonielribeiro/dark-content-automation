_# Guia de Deploy na Nuvem com Render

**Autor**: Manus AI
**Versão**: 1.0
**Data**: 03/12/2025

## 1. Por Que Usar a Nuvem?

Hospedar este sistema na nuvem garante que ele rode **24/7 sem depender do seu computador**. Plataformas como a Render.com oferecem um plano gratuito que é perfeito para este projeto, automatizando a execução e o gerenciamento da infraestrutura.

**Vantagens:**
- **Sempre Ativo**: O agendador roda continuamente na nuvem.
- **Zero Manutenção**: Não precisa se preocupar com servidores ou sistema operacional.
- **Deploy Automático**: Qualquer atualização no seu repositório GitHub pode ser automaticamente publicada.
- **Segurança**: Suas chaves de API são armazenadas de forma segura como variáveis de ambiente.

## 2. Plataforma Recomendada: Render.com

A [Render](https://render.com) é uma plataforma de nuvem (PaaS) que simplifica o deploy de aplicações. O plano gratuito deles inclui um **"Background Worker"**, que é exatamente o que precisamos para rodar nosso script de agendamento em segundo plano.

## 3. Pré-requisitos

1.  **Conta no GitHub**: Onde seu projeto está hospedado.
2.  **Conta na Render**: Crie uma conta gratuita em [dashboard.render.com](https://dashboard.render.com).
3.  **Chaves de API**: Tenha em mãos suas chaves da **OpenAI** e **ElevenLabs**.

## 4. Passo a Passo para o Deploy

### Passo 1: Conecte sua Conta GitHub à Render

Ao criar sua conta na Render, você será solicitado a conectar seu perfil do GitHub. Conceda acesso ao repositório `dark-content-automation` que criamos.

### Passo 2: Crie um Novo "Background Worker"

1.  No painel da Render, clique em **"New +"** e selecione **"Background Worker"**.

    ![New Background Worker](https://i.imgur.com/abcdef.png) <!-- Imagem ilustrativa -->

2.  Na lista de repositórios, selecione `otonielribeiro/dark-content-automation`.

### Passo 3: Configure o Serviço

A Render irá ler o arquivo `render.yaml` que eu criei e pré-configurar a maior parte das opções. Você só precisa preencher alguns campos:

-   **Name**: Dê um nome para o seu serviço (ex: `dark-content-automation`).
-   **Region**: Mantenha a sugestão (ex: `Oregon`).
-   **Branch**: `main`.
-   **Runtime**: `Docker` (já deve estar selecionado).

### Passo 4: Adicione as Variáveis de Ambiente (Segredos)

Esta é a parte mais importante para garantir que o sistema funcione. Role a página até a seção **"Environment"**.

1.  Clique em **"Add Environment Variable"**.
2.  Adicione as seguintes variáveis, uma por uma:

    | Key | Value |
    | :--- | :--- |
    | `OPENAI_API_KEY` | `sua_chave_da_openai_aqui` |
    | `ELEVENLABS_API_KEY` | `sua_chave_da_elevenlabs_aqui` |

    > **Segurança**: A Render criptografa essas variáveis, garantindo que elas não fiquem expostas no seu código.

    ![Environment Variables](https://i.imgur.com/ghjklmn.png) <!-- Imagem ilustrativa -->

### Passo 5: Faça o Deploy

1.  Role até o final da página e clique em **"Create Background Worker"**.

2.  A Render irá buscar seu código no GitHub, construir a imagem Docker e iniciar o serviço. O primeiro deploy pode levar alguns minutos.

### Passo 6: Verifique os Logs

Após o deploy, vá para a aba **"Logs"** do seu serviço na Render. Você verá a saída do script `run_scheduler.py`, indicando que o agendador foi iniciado e a primeira execução do pipeline está em andamento.

```log
Dec 04 10:00:00 AM  ======================================================================
Dec 04 10:00:00 AM  AGENDADOR AUTOMÁTICO INICIADO
Dec 04 10:00:00 AM  ======================================================================
Dec 04 10:00:00 AM  Intervalo: A cada 2 dias
Dec 04 10:00:00 AM  Próxima execução: 2025-12-06 10:00:00.123456
Dec 04 10:00:00 AM
Dec 04 10:00:00 AM  Pressione Ctrl+C para parar
Dec 04 10:00:00 AM  ======================================================================
Dec 04 10:00:00 AM
Dec 04 10:00:01 AM  [2025-12-04 10:00:01] Executando pipeline...
Dec 04 10:00:02 AM  [2025-12-04 10:00:02] 🚀 INICIANDO PIPELINE DE AUTOMAÇÃO
... (logs do pipeline)
```

## 5. Como Funciona a Partir de Agora?

**Pronto!** Seu sistema está 100% autônomo na nuvem.

-   O **Background Worker** na Render executará o script `run_scheduler.py` continuamente.
-   A cada 2 dias, o script irá disparar o `automation_pipeline.py`.
-   Um novo vídeo será gerado e salvo no volume persistente da Render.
-   Se configurado, o vídeo será enviado para o seu YouTube como privado.

Para fazer o upload no TikTok, você pode baixar os vídeos gerados da aba "Shell" do seu serviço na Render ou configurar uma solução de armazenamento externo (como S3) para acessá-los facilmente.

## 6. Alternativa: Railway.app

[Railway](https://railway.app) é outra excelente plataforma similar à Render. O arquivo `railway.json` no repositório permite um deploy igualmente simples. O processo é muito parecido: conecte seu GitHub, crie um novo projeto, e a Railway irá detectar o `Dockerfile` e configurar o serviço. Não se esqueça de adicionar as variáveis de ambiente lá também.
