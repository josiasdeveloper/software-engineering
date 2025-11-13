# Análise de Padrões de Projeto - Vanna 2.0+

Este repositório contém a análise completa de padrões de projeto e arquiteturais implementados no código do [Vanna 2.0+](https://github.com/vanna-ai/vanna), desenvolvida como parte do curso de Engenharia de Software II da Universidade Federal de Sergipe.

## 📋 Motivação

O objetivo deste projeto é identificar e documentar os padrões de projeto (Gang of Four) e padrões arquiteturais presentes no código do Vanna 2.0+, uma biblioteca Python para geração de SQL usando LLMs. A análise combina:

- **Análise manual do código**: Leitura detalhada da codebase para identificar padrões
- **Validação via múltiplos modelos de LLM**: Três modelos diferentes validam cada padrão identificado
- **Documentação estruturada**: Snippets de código, perguntas e respostas organizadas

## 📁 Estrutura do Repositório

```
.
├── DESIGN_PATTERNS_INSUMOS.md      # Snippets, perguntas e respostas (referência)
├── DESIGN_PATTERNS_CONCLUSOES.md   # Análise e conclusões (leitura principal)
├── DESIGN_PATTERNS_ANALYSIS.md     # Documento original completo
├── RELATORIO_PERGUNTAS_INCOMPLETAS.md  # Status de respostas faltantes
│
├── manual-analysis/                # Ferramenta CLI interativa (usada para gerar outputs)
│   └── README.md                   # Documentação da ferramenta
│
├── code-analysis/                  # ⚠️ WORK IN PROGRESS - Análise automatizada
│   └── README.md                   # Status e motivações
│
└── documentation/                  # Documentação e outputs dos modelos
    ├── microsoft_phi.md
    └── Qwen3-Coder-30B-A3B-Instruct.md
```

## 📖 Documentos Principais

### `DESIGN_PATTERNS_CONCLUSOES.md`
**Documento principal para leitura.** Contém:
- Análise em prosa de cada padrão identificado
- Explicação de como e por que cada padrão é usado no Vanna
- Overview dos padrões arquiteturais
- Tabela comparativa da qualidade das respostas das IAs
- Análise qualitativa dos modelos

### `DESIGN_PATTERNS_INSUMOS.md`
**Documento de referência técnica.** Contém:
- Todos os snippets de código organizados
- Perguntas feitas aos modelos
- Respostas completas dos três modelos
- Sistema de índices `X.Y.z` para referência cruzada

### `DESIGN_PATTERNS_ANALYSIS.md`
Documento original completo com toda a análise detalhada.

## 🎯 Padrões Identificados

### Padrões de Projeto (9)
1. **Strategy Pattern** - Intercambiabilidade de LLMs, autenticação, workflows
2. **Template Method** - Estrutura comum para tools e componentes
3. **Abstract Factory** - Criação de componentes de UI
4. **Adapter Pattern** - Compatibilidade com código legacy
5. **Chain of Responsibility** - Middlewares e lifecycle hooks
6. **Observer Pattern** - Observabilidade e monitoramento
7. **Registry Pattern** - Acesso centralizado a tools e componentes
8. **Builder Pattern** - Construção incremental de prompts
9. **Dependency Injection** - Injeção de todas as dependências

### Padrões Arquiteturais (4)
1. **Plugin Architecture / Hexagonal Architecture** - Core isolado de implementações
2. **Layered Architecture (N-Tier)** - Separação em camadas
3. **Event-Driven Architecture** - Streams assíncronos de eventos
4. **Pipeline Architecture** - Processamento em estágios sequenciais

## 🛠️ Ferramentas

### `manual-analysis/`
Ferramenta CLI interativa usada para gerar os outputs dos modelos LLM. Permite análise manual de código através de chat interativo com modelos locais.

**Uso**: Foi utilizado para fazer perguntas aos modelos sobre padrões específicos, gerando as respostas documentadas em `DESIGN_PATTERNS_INSUMOS.md`.

### `code-analysis/` ⚠️ WORK IN PROGRESS
Ferramenta de análise automatizada que clona repositórios e usa LLM para detectar padrões automaticamente.

**Status**: Em desenvolvimento, não concluído. Veja `code-analysis/README.md` para detalhes sobre motivações e progresso.

## 📊 Metodologia

1. **Identificação Manual**: Análise detalhada do código fonte do Vanna 2.0+
2. **Estratégias de Validação**: Múltiplas estratégias por padrão com snippets ordenados
3. **Validação Cruzada**: Três modelos diferentes validam cada padrão
4. **Documentação**: Organização em sistema de índices `X.Y.z` para referência

## 📝 Modelos Utilizados

- **deepseek-ai/deepseek-coder-6.7b-instruct**: Especializado em código, excelente em padrões de projeto
- **microsoft/phi-2**: Modelo compacto, cobertura ampla mas menor precisão
- **Qwen/Qwen2.5-Coder-32B-Instruct**: Grande escala, alta precisão em padrões de projeto

## 📄 Licença

MIT License - Veja arquivo LICENSE para detalhes.
