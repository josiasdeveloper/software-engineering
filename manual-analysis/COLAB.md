# Guia Completo: Usando `run.ipynb` no Google Colab

Este guia detalha como usar o notebook `run.ipynb` para análise interativa de padrões de projeto usando modelos LLM no Google Colab.

## 📋 Visão Geral

O notebook `run.ipynb` é uma interface otimizada para Google Colab que permite:
- Carregar modelos LLM especializados em código (DeepSeek Coder, Phi-2, etc.)
- Fazer análise interativa de padrões de projeto
- Salvar conversas automaticamente com timestamp
- Baixar conversas salvas diretamente do Colab

## 🎯 Pré-requisitos

1. **Conta Google** com acesso ao Google Colab
2. **GPU Runtime** (recomendado): Para modelos maiores como DeepSeek Coder 6.7B
   - No Colab: Runtime → Change runtime type → GPU (T4 ou superior)
   - GPU gratuita disponível, mas com limitações de tempo

## 🚀 Passo a Passo Detalhado

### Passo 1: Abrir o Notebook no Colab

1. Acesse o Google Colab: https://colab.research.google.com/
2. Faça upload do arquivo `run.ipynb` ou clone o repositório:
   ```python
   !git clone https://github.com/josiasdeveloper/software-engineering.git
   %cd software-engineering/manual-analysis
   ```

### Passo 2: Configurar o Modelo (Célula 1)

**O que faz**: Define qual modelo LLM será usado para análise.

```python
import os

# Opção 1: DeepSeek Coder (recomendado - melhor qualidade)
MODEL = "deepseek-ai/deepseek-coder-6.7b-instruct"

# Opção 2: Phi-2 (menor, mais rápido, menos preciso)
# MODEL = "microsoft/phi-2"

os.environ['LLM_MODEL'] = MODEL
print(f"Model configured: {MODEL}")
```

**Escolha do modelo**:
- **DeepSeek Coder 6.7B**: Melhor para análise detalhada, requer ~15GB GPU
- **Phi-2**: Mais rápido, menor memória, útil para testes rápidos

**Dica**: Se o modelo não carregar por falta de memória, use `microsoft/phi-2`.

### Passo 3: Clonar/Atualizar Repositório (Célula 2)

**O que faz**: Garante que você tem o código mais recente do repositório.

```python
import os

REPO_URL = "https://github.com/josiasdeveloper/software-engineering.git"

if os.path.exists('software-engineering'):
    print("Repository exists, updating...")
    %cd software-engineering/manual-analysis
    !git pull
else:
    print("Cloning repository...")
    !git clone {REPO_URL}
    %cd software-engineering/manual-analysis

print("\nReady!")
```

**Comportamento**:
- Se o repositório já existe, atualiza (`git pull`)
- Se não existe, clona do zero
- Sempre navega para `manual-analysis/` ao final

**Nota**: Se você já está no diretório correto, pode pular esta célula.

### Passo 4: Instalar Dependências (Célula 3)

**O que faz**: Instala o pacote `manual-analysis` em modo desenvolvimento.

```python
!pip install -e . -q
```

**O que acontece**:
- Instala todas as dependências listadas em `requirements.txt`
- Instala o pacote em modo editável (`-e`)
- Flag `-q` reduz verbosidade

**Tempo estimado**: 1-2 minutos na primeira execução.

**Troubleshooting**:
- Se der erro, tente: `!pip install -e . --no-cache-dir`
- Verifique se está no diretório correto: `!pwd`

### Passo 5: Executar Chat Interativo (Célula 4)

**O que faz**: Inicia o chat interativo com o modelo LLM.

```python
!chat
```

**O que acontece**:
1. Carrega o modelo LLM (pode levar 1-3 minutos na primeira vez)
2. Mostra banner de boas-vindas
3. Inicia loop interativo de chat

**Primeira execução**: O modelo será baixado do Hugging Face (~13GB para DeepSeek Coder).

## 💬 Comandos Disponíveis no Chat

Durante o chat, você pode usar os seguintes comandos:

### `/help`
Mostra ajuda completa com todos os comandos e dicas de uso.

**Uso**: Digite `/help` e pressione Enter.

### `/clear`
Limpa o histórico de conversa, mas mantém o modelo carregado.

**Quando usar**: 
- Quando quiser começar uma nova análise sem perder o modelo carregado
- Para liberar contexto sem recarregar o modelo

**Uso**: Digite `/clear` e pressione Enter.

### `/restart`
Reinicia o modelo completamente e limpa todo o contexto.

**Quando usar**:
- Quando o modelo está com comportamento estranho
- Para liberar memória GPU completamente
- Após mudar configurações

**Uso**: Digite `/restart` e pressione Enter.

**Nota**: O modelo será recarregado na próxima mensagem (pode demorar).

### `/save`
Salva a conversa atual em um arquivo com timestamp automático.

**Formato do arquivo**: `conversation_YYYYMMDD_HHMMSS.txt`

**Quando usar**:
- Ao final de uma sessão de análise
- Antes de fazer `/restart` ou `/clear`
- Para manter registro das respostas do modelo

**Uso**: Digite `/save` e pressione Enter.

**Exemplo de saída**:
```
Conversation saved to: conversation_51215_143022.txt
```

### `/context`
Mostra informações sobre o uso atual do contexto.

**Informações exibidas**:
- Porcentagem de tokens usados (com barra visual)
- Número atual de tokens
- Número máximo de tokens
- Quantidade de mensagens
- Se há resumo ativo

**Quando usar**:
- Para verificar se está próximo do limite
- Para entender quando o resumo automático será ativado

**Uso**: Digite `/context` e pressione Enter.

**Exemplo de saída**:
```
Current Context Usage
Token Usage: [████████████████████░░░░░░░░░░░░░░░░░░░░] 45.2%
- Current: 7,234 tokens
- Maximum: 16,000 tokens

Messages: 8
Has Summary: No
```

### `/raw`
Mostra a última resposta do assistente em texto puro (sem formatação).

**Quando usar**:
- Para copiar facilmente a resposta
- Quando precisa do texto sem markdown
- Para colar em outros documentos

**Uso**: Digite `/raw` e pressione Enter.

### `/exit`
Sai do chat interativo.

**Uso**: Digite `/exit` e pressione Enter.

**Nota**: O modelo permanece carregado na memória até reiniciar o runtime.

## 📝 Modos de Entrada

### Entrada Simples (Uma Linha)
Simplesmente digite sua pergunta e pressione Enter:

```
You: What design patterns are used in this code?
```

### Entrada Multi-linha (Código)
Para colar código ou fazer perguntas longas:

1. Digite `begin` e pressione Enter
2. Cole ou digite seu código (múltiplas linhas)
3. Digite `end` em uma nova linha e pressione Enter

**Exemplo**:
```
You: begin
class MyClass:
    def __init__(self):
        self.value = 10
end
```

**Dica**: Você também pode simplesmente colar código diretamente - o sistema detecta múltiplas linhas automaticamente.

## 🎯 Exemplos de Uso

### Exemplo 1: Análise de Padrão Strategy

```
You: begin
# src/vanna/core/llm/base.py
from abc import ABC, abstractmethod

class LlmService(ABC):
    @abstractmethod
    async def send_request(self, request: LlmRequest) -> LlmResponse:
        pass

# src/vanna/integrations/anthropic/llm.py
class AnthropicLlmService(LlmService):
    async def send_request(self, request: LlmRequest) -> LlmResponse:
        # Implementação específica do Anthropic
        pass

# src/vanna/integrations/openai/llm.py
class OpenAILlmService(LlmService):
    async def send_request(self, request: LlmRequest) -> LlmResponse:
        # Implementação específica do OpenAI
        pass
end

You: Estas duas classes implementam qual padrão de projeto em relação à interface abstrata anterior?
```

### Exemplo 2: Pergunta Direta

```
You: Como o Template Method Pattern é usado na classe Tool?
```

### Exemplo 3: Análise com Contexto

```
You: Analise este código e identifique padrões de projeto:
[cole o código aqui]

You: Como este padrão facilita a extensibilidade?
```

## 📥 Passo 6: Baixar Conversas Salvas (Célula 5)

**O que faz**: Localiza e baixa todos os arquivos de conversa salvos.

```python
import os
import glob

# Encontra todos os arquivos de conversa
conversation_files = glob.glob('conversation_*.txt')

if not conversation_files:
    print("No conversation files found.")
    print("Make sure to use /save command in the chat first.")
else:
    print(f"Found {len(conversation_files)} conversation file(s):")
    for f in conversation_files:
        print(f"  - {f}")
    
    # Tenta baixar se estiver no Colab
    try:
        from google.colab import files
        print("\nDownloading files...")
        for f in conversation_files:
            files.download(f)
        print("\nAll conversations downloaded!")
    except ImportError:
        print("\nNot running in Google Colab.")
        print("Files are saved in the current directory.")
```

**Comportamento**:
- Lista todos os arquivos `conversation_*.txt` no diretório atual
- Se estiver no Colab, baixa automaticamente cada arquivo
- Se não estiver no Colab, apenas mostra os arquivos encontrados

**Quando usar**:
- Ao final de uma sessão de análise
- Antes de desconectar do Colab
- Para fazer backup das conversas

**Dica**: Execute esta célula antes de desconectar do runtime para não perder as conversas.

## 🔧 Configurações Avançadas

### Alterar Modelo Durante Execução

Você pode mudar o modelo editando `src/manual/config.py`:

```python
MODEL_NAME = "microsoft/phi-2"  # Mude aqui
MAX_CONTEXT_TOKENS = 16000
SUMMARIZE_THRESHOLD = 0.7
```

Depois, use `/restart` no chat para recarregar.

### Ajustar Limites de Contexto

Edite `src/manual/config.py`:

```python
MAX_CONTEXT_TOKENS = 32000  # Aumenta para modelos maiores
SUMMARIZE_THRESHOLD = 0.8   # Resumir quando usar 80% do contexto
```

### Resumo Automático

O sistema automaticamente resume conversas longas quando:
- O uso de tokens excede `SUMMARIZE_THRESHOLD` (padrão: 70%)
- Há mais de `MAX_HISTORY_BEFORE_SUMMARY` mensagens (padrão: 10)

Isso preserva o contexto importante enquanto libera espaço.

## ⚠️ Troubleshooting

### Problema: Modelo não carrega / Erro de memória

**Solução 1**: Use um modelo menor
```python
MODEL = "microsoft/phi-2"
```

**Solução 2**: Reinicie o runtime
- Runtime → Restart runtime
- Execute novamente as células

**Solução 3**: Verifique o tipo de GPU
- Runtime → Change runtime type
- Selecione GPU (T4 ou superior)

### Problema: Chat não responde / Trava

**Solução**: Use `/restart` para reiniciar o modelo.

### Problema: Conversas não são salvas

**Verifique**:
1. Você usou `/save` no chat?
2. Está no diretório correto? (`manual-analysis/`)
3. Permissões de escrita no Colab

**Solução**: Execute `!pwd` para verificar o diretório atual.

### Problema: Dependências não instalam

**Solução**:
```python
!pip install --upgrade pip
!pip install -e . --no-cache-dir
```

### Problema: Git clone falha

**Solução**: Verifique conexão com internet:
```python
!ping -c 3 github.com
```

## 💡 Dicas e Boas Práticas

### 1. Salve Frequentemente
Use `/save` regularmente para não perder trabalho se o runtime desconectar.

### 2. Monitore o Contexto
Use `/context` periodicamente para evitar surpresas com resumo automático.

### 3. Use `/raw` para Copiar
Quando precisar copiar respostas, use `/raw` para obter texto limpo.

### 4. Organize Suas Perguntas
Faça perguntas específicas e bem estruturadas para melhores respostas.

### 5. Use Multi-linha para Código
Para código longo, use o modo `begin`/`end` para melhor formatação.

### 6. Baixe Antes de Desconectar
Sempre execute a célula de download antes de desconectar do Colab.

### 7. Limite de Tempo do Colab
- Runtime gratuito: ~12 horas contínuas
- Desconexão automática após inatividade
- Salve e baixe conversas regularmente

## 📊 Fluxo de Trabalho Recomendado

1. **Configurar**: Execute células 1-3 (configuração, clone, instalação)
2. **Iniciar Chat**: Execute célula 4 (`!chat`)
3. **Análise**: Faça suas perguntas e análises
4. **Salvar**: Use `/save` periodicamente
5. **Baixar**: Execute célula 5 antes de desconectar
6. **Documentar**: Use as conversas salvas para documentação

## 🔗 Recursos Adicionais

- **README.md**: Documentação geral da ferramenta
- **src/manual/config.py**: Todas as configurações disponíveis
- **src/manual/command.py**: Código fonte dos comandos
- **documentation/DESIGN_PATTERNS_INSUMOS.md**: Exemplos de análises realizadas

## 📄 Estrutura dos Arquivos de Conversa

Os arquivos salvos com `/save` contêm:
- Timestamp da conversa
- Todas as mensagens do usuário
- Todas as respostas do assistente
- Formatação markdown preservada

**Formato**:
```
=== Conversation History ===
Timestamp: 2025-12-15 14:30:22

[User]: Pergunta do usuário
[Assistant]: Resposta do modelo

[User]: Próxima pergunta
[Assistant]: Próxima resposta
...
```

## 🎓 Casos de Uso

### Análise de Padrões de Projeto
1. Cole snippets de código
2. Pergunte sobre padrões específicos
3. Peça explicações detalhadas
4. Valide identificações

### Validação Cruzada
1. Analise o mesmo código com diferentes modelos
2. Compare respostas
3. Identifique consensos e divergências

### Documentação
1. Use `/raw` para copiar respostas
2. Organize em documentos estruturados
3. Referencie índices `X.Y.z` do sistema de documentação

## 📝 Notas Finais

- O notebook é otimizado para Google Colab, mas pode funcionar localmente
- Modelos grandes requerem GPU - use runtime com GPU habilitada
- Salve frequentemente - runtime pode desconectar após inatividade
- Use `/context` para monitorar uso de recursos
- Respostas são geradas em markdown - use `/raw` para texto puro

---

**Última atualização**: Dezembro 2025
**Versão**: 1.0

