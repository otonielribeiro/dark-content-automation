#!/usr/bin/env python3
"""
Sistema de Geração Automatizada de Conteúdo - Casos Policiais Reais
Autor: Manus AI
Data: 03/12/2025
"""

import os
import json
import random
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# Configurações
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
LOGS_DIR = BASE_DIR / "logs"

class ContentGenerator:
    """Gerador automatizado de roteiros para casos policiais"""
    
    def __init__(self):
        # Configura OpenRouter API
        api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.cases_db = self.load_cases_database()
        
    def load_cases_database(self):
        """Carrega banco de dados de casos policiais"""
        cases_file = DATA_DIR / "casos_policiais.json"
        if cases_file.exists():
            with open(cases_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def select_random_case(self):
        """Seleciona um caso aleatório que ainda não foi usado"""
        used_cases_file = DATA_DIR / "casos_usados.json"
        
        # Carrega casos já usados
        if used_cases_file.exists():
            with open(used_cases_file, 'r', encoding='utf-8') as f:
                used_cases = json.load(f)
        else:
            used_cases = []
        
        # Filtra casos disponíveis
        available_cases = [c for c in self.cases_db if c['id'] not in used_cases]
        
        if not available_cases:
            # Se todos foram usados, reinicia
            used_cases = []
            available_cases = self.cases_db
        
        # Seleciona aleatoriamente
        selected = random.choice(available_cases)
        
        # Marca como usado
        used_cases.append(selected['id'])
        with open(used_cases_file, 'w', encoding='utf-8') as f:
            json.dump(used_cases, f, ensure_ascii=False, indent=2)
        
        return selected
    
    def generate_script(self, case_data):
        """Gera roteiro cinematográfico usando GPT-4"""
        
        prompt = f"""Você é um roteirista especializado em documentários criminais para TikTok/YouTube Shorts.

CASO: {case_data['titulo']}
RESUMO: {case_data['resumo']}
DATA: {case_data['data']}
LOCAL: {case_data['local']}

Crie um roteiro CINEMATOGRÁFICO e IMPACTANTE para um vídeo de 60-90 segundos seguindo esta estrutura:

1. HOOK (3-5 segundos): Frase de abertura extremamente impactante que prenda a atenção imediatamente
2. CONTEXTO (15-20 segundos): Apresente o caso, data, local e personagens principais
3. DESENVOLVIMENTO (25-35 segundos): Descreva os eventos principais do caso com tensão crescente
4. CLÍMAX (10-15 segundos): O momento mais chocante ou revelação
5. CONCLUSÃO (5-10 segundos): Desfecho ou pergunta reflexiva que gere engajamento

REQUISITOS:
- Tom sério, contemplativo e misterioso
- Linguagem cinematográfica e envolvente
- Frases curtas e impactantes
- SEM emojis ou linguagem informal
- Terminar com pergunta ou afirmação que provoque comentários
- Texto APENAS para narração (sem indicações de cena)
- Máximo 200 palavras

ROTEIRO:"""

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Modelo via OpenRouter
            messages=[
                {"role": "system", "content": "Você é um roteirista especializado em documentários criminais dark e cinematográficos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        script = response.choices[0].message.content.strip()
        return script
    
    def generate_visual_prompts(self, case_data, script):
        """Gera prompts para geração de visuais cinematográficos"""
        
        prompt = f"""Com base neste roteiro de caso policial, crie 4 PROMPTS para geração de imagens/vídeos cinematográficos com IA.

ROTEIRO:
{script}

CASO: {case_data['titulo']}

Crie 4 prompts em INGLÊS para Runway Gen-3 ou Midjourney que capturem:
1. Cena de abertura (atmosfera dark e misteriosa)
2. Contexto/localização do crime
3. Momento de tensão/investigação
4. Cena final reflexiva

REQUISITOS para cada prompt:
- Estilo: cinematic, dark atmosphere, film noir, dramatic lighting
- Qualidade: photorealistic, 8k, professional cinematography
- Movimento: slow motion, smooth camera movement
- Paleta: dark colors, moody, noir aesthetic
- SEM pessoas identificáveis (usar silhuetas, sombras)
- SEM texto ou números na imagem

Retorne APENAS os 4 prompts, um por linha, numerados."""

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Modelo via OpenRouter
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        prompts_text = response.choices[0].message.content.strip()
        prompts = [p.strip() for p in prompts_text.split('\n') if p.strip() and p[0].isdigit()]
        
        # Remove numeração
        prompts = [p.split('.', 1)[1].strip() if '.' in p else p for p in prompts]
        
        return prompts[:4]
    
    def generate_metadata(self, case_data, script):
        """Gera título, descrição e hashtags para o vídeo"""
        
        prompt = f"""Crie metadados para este vídeo de caso policial:

CASO: {case_data['titulo']}
ROTEIRO: {script[:200]}...

Gere:
1. TÍTULO: Chamativo e misterioso (máx 60 caracteres)
2. DESCRIÇÃO: Breve descrição para YouTube/TikTok (máx 150 caracteres)
3. HASHTAGS: 8-10 hashtags relevantes em português

Formato de resposta:
TÍTULO: [seu título]
DESCRIÇÃO: [sua descrição]
HASHTAGS: #tag1 #tag2 #tag3..."""

        response = self.client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Modelo via OpenRouter
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        metadata_text = response.choices[0].message.content.strip()
        
        # Parse metadata
        metadata = {}
        for line in metadata_text.split('\n'):
            if line.startswith('TÍTULO:'):
                metadata['titulo'] = line.replace('TÍTULO:', '').strip()
            elif line.startswith('DESCRIÇÃO:'):
                metadata['descricao'] = line.replace('DESCRIÇÃO:', '').strip()
            elif line.startswith('HASHTAGS:'):
                metadata['hashtags'] = line.replace('HASHTAGS:', '').strip()
        
        return metadata
    
    def save_content_package(self, case_data, script, visual_prompts, metadata):
        """Salva pacote completo de conteúdo"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"video_{timestamp}.json"
        
        package = {
            "timestamp": timestamp,
            "caso_id": case_data['id'],
            "caso_titulo": case_data['titulo'],
            "script": script,
            "visual_prompts": visual_prompts,
            "metadata": metadata,
            "status": "gerado"
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, ensure_ascii=False, indent=2)
        
        # Log
        log_file = LOGS_DIR / f"log_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.now()}] Conteúdo gerado: {output_file.name}\n")
        
        return output_file
    
    def generate_complete_content(self):
        """Pipeline completo de geração de conteúdo"""
        
        print("🎬 Iniciando geração de conteúdo...")
        
        # 1. Seleciona caso
        print("📁 Selecionando caso policial...")
        case = self.select_random_case()
        print(f"✅ Caso selecionado: {case['titulo']}")
        
        # 2. Gera roteiro
        print("📝 Gerando roteiro cinematográfico...")
        script = self.generate_script(case)
        print(f"✅ Roteiro gerado ({len(script.split())} palavras)")
        
        # 3. Gera prompts visuais
        print("🎨 Gerando prompts visuais...")
        visual_prompts = self.generate_visual_prompts(case, script)
        print(f"✅ {len(visual_prompts)} prompts visuais gerados")
        
        # 4. Gera metadados
        print("📊 Gerando metadados...")
        metadata = self.generate_metadata(case, script)
        print(f"✅ Metadados gerados")
        
        # 5. Salva pacote
        print("💾 Salvando pacote de conteúdo...")
        output_file = self.save_content_package(case, script, visual_prompts, metadata)
        print(f"✅ Pacote salvo: {output_file}")
        
        print("\n🎉 Conteúdo gerado com sucesso!")
        print(f"\n📄 ROTEIRO:\n{script}\n")
        print(f"📊 METADADOS:")
        print(f"   Título: {metadata.get('titulo', 'N/A')}")
        print(f"   Hashtags: {metadata.get('hashtags', 'N/A')}")
        
        return output_file


if __name__ == "__main__":
    generator = ContentGenerator()
    generator.generate_complete_content()
