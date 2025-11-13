# Manual Analysis Tool

Ferramenta CLI interativa para análise manual de padrões de projeto usando modelos LLM locais.

## 🎯 Propósito

Esta ferramenta foi utilizada para gerar os outputs dos modelos LLM documentados em `DESIGN_PATTERNS_INSUMOS.md`. Permite análise interativa de código através de chat com modelos especializados em código.

## 🚀 Uso Rápido

```bash
# Instalação
make install-dev

# Executar
make chat
# ou
chat
```

## 📋 Funcionalidades

- **Chat interativo** com modelo LLM especializado em análise de código
- **Gerenciamento de contexto** automático com resumo de conversas longas
- **Histórico persistente** de conversações
- **Comandos úteis** para salvar, limpar contexto, verificar uso de tokens

## 🏗️ Arquitetura

```
src/manual/
├── command.py         # CLI entry point e loop interativo
├── orchestrator.py    # Orquestração de conversas e contexto
├── llm_manager.py     # Carregamento e geração do modelo (Singleton)
├── summarizer.py      # Resumo automático de conversas
└── config.py          # Configurações (modelo, tokens, thresholds)
```

## 💻 Comandos Disponíveis

- `/help` - Mostra ajuda
- `/clear` - Limpa histórico (mantém modelo carregado)
- `/restart` - Reinicia modelo e limpa contexto (libera GPU)
- `/save` - Salva conversa com timestamp automático
- `/context` - Mostra uso atual de contexto (tokens, mensagens)
- `/exit` - Sai do assistente

## ⚙️ Configuração

Edite `src/manual/config.py`:

```python
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-instruct"
MAX_CONTEXT_TOKENS = 16000
SUMMARIZE_THRESHOLD = 0.7  # Resumir quando usar 70% do contexto
MAX_HISTORY_BEFORE_SUMMARY = 10
```

## 📝 Como Foi Usado

Esta ferramenta foi utilizada para:

1. Analisar snippets de código do Vanna 2.0+
2. Fazer perguntas específicas sobre padrões de projeto
3. Gerar respostas dos modelos que foram documentadas
4. Validar identificação de padrões através de múltiplos modelos

As conversas foram salvas e suas respostas extraídas para compor `DESIGN_PATTERNS_INSUMOS.md`.

## 🔧 Requisitos

- Python 3.8+
- GPU CUDA (~15GB para DeepSeek Coder 6.7B)
- Ou uso em Google Colab (ver `run.ipynb`)

## 📚 Uso em Notebook

O arquivo `run.ipynb` é otimizado para Google Colab:

1. Configure o modelo via variável de ambiente
2. Clone/atualize repositório
3. Instale dependências: `pip install -e .`
4. Execute `!chat` para iniciar
5. Use `/save` para salvar conversas
6. Baixe conversas salvas automaticamente

## 🧹 Desenvolvimento

```bash
# Limpar cache
make clean

# Limpar tudo incluindo venv
make clean-all

# Reinstalar
make install-dev
```

## 📄 Licença

MIT License - Veja LICENSE no diretório raiz.
