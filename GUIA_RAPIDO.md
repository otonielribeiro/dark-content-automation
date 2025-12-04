# 🚀 Guia Rápido de Início

## ⚡ Começando em 5 Passos

### 1️⃣ Configure as APIs

```bash
# OpenRouter (para geração de roteiros)
export OPENROUTER_API_KEY='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'

# ElevenLabs (para narração)
export ELEVENLABS_API_KEY='sua_chave_aqui'
```

💡 **Obtenha suas chaves em**:
- OpenRouter: [openrouter.ai/keys](https://openrouter.ai/keys)
- ElevenLabs: [elevenlabs.io](https://elevenlabs.io)

---

### 2️⃣ Teste a Geração de Conteúdo

```bash
cd /home/ubuntu/dark_content_automation
python3 scripts/content_generator.py
```

✅ Isso irá gerar um roteiro e salvá-lo em `output/`

---

### 3️⃣ Gere a Narração

```bash
# Substitua pelo arquivo gerado no passo anterior
python3 scripts/voice_generator.py output/video_TIMESTAMP.json
```

✅ Um arquivo MP3 será criado

---

### 4️⃣ Compile o Vídeo

```bash
python3 scripts/video_compiler.py output/video_TIMESTAMP.json
```

✅ Seu primeiro vídeo estará pronto em `output/final_TIMESTAMP.mp4`

---

### 5️⃣ Execute o Pipeline Completo

```bash
# Tudo de uma vez!
python3 scripts/automation_pipeline.py
```

✅ Gera roteiro + narração + vídeo automaticamente

---

## 🤖 Automação Total

### Método Simples (Recomendado)

```bash
# Inicia agendador em background
nohup python3 run_scheduler.py > scheduler.log 2>&1 &

# Para parar
pkill -f run_scheduler.py
```

---

## 📊 Estrutura de Custos

| Item | Custo por Vídeo | Custo Mensal (15 vídeos) |
|------|----------------|-------------------------|
| OpenRouter (GPT-4o-mini) | ~$0.01 | ~$0.15 |
| ElevenLabs | ~$0.30 | ~$4.50 |
| **TOTAL** | **~$0.31** | **~$4.65** |

💰 **Menos de R$ 25/mês** para 15 vídeos automatizados!

---

## 🎯 Checklist de Configuração

- [ ] Configurei `ELEVENLABS_API_KEY`
- [ ] Testei geração de conteúdo
- [ ] Testei geração de narração
- [ ] Testei compilação de vídeo
- [ ] Executei pipeline completo
- [ ] (Opcional) Configurei credenciais do YouTube
- [ ] Iniciei o agendador automático

---

## 🆘 Problemas Comuns

### "OPENROUTER_API_KEY não configurada"
```bash
export OPENROUTER_API_KEY='sk-or-v1-...'
```

### "ELEVENLABS_API_KEY não configurada"
```bash
export ELEVENLABS_API_KEY='sua_chave'
```

### "FFmpeg não encontrado"
```bash
sudo apt install ffmpeg
```

### "Erro ao gerar vídeo"
Verifique se o arquivo de áudio foi gerado corretamente no passo anterior.

---

## 📱 Upload para TikTok

**TikTok não possui API oficial pública**. Opções:

1. **Upload Manual** (Recomendado)
   - Abra o app TikTok
   - Faça upload do vídeo de `output/final_TIMESTAMP.mp4`
   - Use os metadados do arquivo JSON (título, hashtags)

2. **Ferramentas de Terceiros**
   - [Publer](https://publer.io)
   - [Buffer](https://buffer.com)
   - [Later](https://later.com)

---

## 🎬 Próximos Passos

1. **Adicione mais casos** em `data/casos_policiais.json`
2. **Customize a voz** em `scripts/voice_generator.py`
3. **Adicione música de fundo** em `assets/background_music.mp3`
4. **Configure upload do YouTube** (opcional)
5. **Inicie o agendador** para automação total

---

**Pronto para criar conteúdo dark automatizado! 🌑**
