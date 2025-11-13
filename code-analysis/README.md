# Code Analysis - Automated Pattern Detection

⚠️ **WORK IN PROGRESS** - Esta ferramenta está em desenvolvimento e **não foi concluída**.

## 🎯 Objetivo

Ferramenta automatizada para detectar padrões de projeto em codebases usando LLMs. O objetivo é automatizar o processo de análise que foi feito manualmente para o projeto do Vanna 2.0+.

## ⚠️ Status Atual

**Não concluído.** A análise do Vanna 2.0+ foi realizada manualmente usando a ferramenta `manual-analysis/`, que permitiu análise interativa e controle fino sobre as perguntas feitas aos modelos.

## 💡 Motivação

A ideia inicial era criar uma ferramenta que:
1. Clona repositórios automaticamente
2. Gera árvore de diretórios
3. Usa LLM para resumir arquivos
4. Detecta padrões de projeto automaticamente

No entanto, durante o desenvolvimento do projeto, descobrimos que a análise manual oferecia:
- **Melhor controle** sobre quais padrões investigar
- **Perguntas mais específicas** e contextualizadas
- **Validação mais precisa** através de múltiplas estratégias
- **Resultados de maior qualidade** para documentação

## 🏗️ Arquitetura Planejada

```
src/
├── analyzer.py         # Orquestrador principal
├── repository.py       # Gerenciamento de repositórios Git
├── tree_builder.py     # Construção de árvore de diretórios
├── file_reader.py      # Leitura e filtragem de arquivos
├── indexer.py          # Geração de resumos via LLM
├── llm_manager.py      # Gerenciamento do modelo LLM
└── commands.py         # CLI commands
```

## 🚧 Funcionalidades Implementadas

- ✅ Clone de repositórios Git
- ✅ Geração de árvore de diretórios
- ✅ Identificação de arquivos fonte
- ✅ Carregamento de modelos LLM
- ✅ Geração de resumos de arquivos
- ❌ Detecção automática de padrões (não implementado)
- ❌ Análise cruzada de padrões (não implementado)

## 📋 Como Usar (Se Implementado)

```bash
# Instalação
pip install -e .

# Carregar modelo (fazer uma vez)
analyze load-model

# Clonar e mapear repositório
analyze clone https://github.com/vanna-ai/vanna.git

# Gerar resumos de arquivos
analyze index

# Análise de padrões (não implementado)
analyze patterns
```

## 🔧 Requisitos

- Python 3.12+
- GPU recomendada (Google Colab T4 ou melhor)
- Conexão com internet para download de modelos

## 📝 Uso em Google Colab

Ver `COLAB_SETUP.md` para instruções detalhadas de setup em Colab.

## 🎓 Lições Aprendidas

Durante o desenvolvimento, aprendemos que:

1. **Análise manual** oferece melhor qualidade para documentação acadêmica
2. **Múltiplas estratégias** por padrão são essenciais para validação
3. **Contexto específico** é mais importante que análise genérica
4. **Validação cruzada** com múltiplos modelos aumenta confiabilidade

Por isso, a análise do Vanna foi concluída usando `manual-analysis/` em vez desta ferramenta automatizada.

## 📄 Licença

MIT License - Veja LICENSE no diretório raiz.
