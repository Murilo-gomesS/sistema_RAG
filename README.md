# Sistema RAG para Consultas Acadêmicas

> Aplicação inteligente baseada em RAG (Retrieval-Augmented Generation) para responder perguntas sobre o curso de Desenvolvimento de Software Multiplataforma da Fatec Jacareí.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Requisitos Atendidos](#requisitos-atendidos)
- [Arquitetura da Solução](#arquitetura-da-solução)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Modelo de Linguagem](#modelo-de-linguagem)
- [Implementação do RAG](#implementação-do-rag)
- [Limitações](#limitações)
- [Exemplo de Uso](#exemplo-de-uso)
- [Documentação Completa](#documentação-completa)

## 🎯 Sobre o Projeto

Este projeto implementa um assistente virtual educacional utilizando técnicas modernas de Processamento de Linguagem Natural (NLP) e Busca Semântica. O sistema integra:

- **RAG (Retrieval-Augmented Generation)**: Busca informações relevantes em uma base de conhecimento antes de processar respostas
- **LLM (Large Language Model)**: Usa o Meta-Llama-3-8B-Instruct para criar respostas naturais e precisas
- **Indexação Vetorial**: Utiliza FAISS com embeddings semânticos para busca eficiente de informações

O assistente é especializado em fornecer informações sobre o curso de Desenvolvimento de Software Multiplataforma (DSM) da Fatec Jacareí.

## 🚀 Tecnologias Utilizadas

### Linguagem
- **Python 3.8+**: Linguagem principal do projeto

### Frameworks e Bibliotecas
- **FastAPI**: Framework web moderno e rápido para construção de APIs REST
- **Uvicorn**: Servidor ASGI de alto desempenho para aplicações assíncronas
- **Sentence Transformers**: Biblioteca para geração de embeddings semânticos de alta qualidade
- **FAISS**: Biblioteca otimizada de busca vetorial desenvolvida pela Meta AI
- **Requests**: Cliente HTTP robusto para integração com APIs externas
- **Pydantic**: Framework para validação de dados e serialização automática

### Serviços Externos
- **Hugging Face API**: Acesso ao modelo Meta-Llama-3-8B-Instruct
- **Sentence Transformers Hub**: Modelo de embeddings all-MiniLM-L6-v2

## ✅ Requisitos Atendidos

### 1. Implementação Técnica
✓ **Linguagem**: Projeto desenvolvido inteiramente em Python  
✓ **Funções**: Implementadas funções para entrada de perguntas (`process_question`) e geração de respostas (`generate_llm_response`)  
✓ **Execução**: Código carrega e executa o LLM via API do Hugging Face

### 2. Modelo de Linguagem (LLM)
✓ **Gratuito**: Utiliza Meta-Llama-3-8B-Instruct via Hugging Face (gratuito)  
✓ **Execução**: Consumido via API REST do Hugging Face Router

### 3. Mecanismo de RAG
✓ **Base de Conhecimento**: Textos sobre o curso DSM da Fatec Jacareí  
✓ **Processamento**: Sistema indexa documentos usando embeddings e FAISS  
✓ **Integração**: Informações recuperadas são incorporadas no prompt enviado ao LLM

### 4. Documentação
✓ **Documento Explicativo**: `documentacao_chatbot_dsm.md` contém:
  - Modelo escolhido e justificativa
  - Detalhamento da implementação do RAG
  - Limitações da solução
  - Exemplo de diálogo com 5 interações

### 5. Formato de Entrega
✓ **Individual**: Trabalho desenvolvido individualmente  
✓ **Arquivos Python**: `app.py` (script principal)  
✓ **Documentação**: Arquivo markdown com explicações completas  
✓ **Sem Compactação**: Arquivos entregues sem .zip ou .rar

## 🏗️ Arquitetura da Solução

```
┌─────────────────┐
│   Usuário       │
└────────┬────────┘
         │ POST /ask
         ▼
┌─────────────────────────────────────┐
│     FastAPI Application             │
│  ┌──────────────────────────────┐  │
│  │  1. Recebe Pergunta          │  │
│  └──────────┬───────────────────┘  │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  2. Vetoriza com             │  │
│  │     SentenceTransformer      │  │
│  └──────────┬───────────────────┘  │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  3. Busca no Índice FAISS    │  │
│  │     (documento mais similar) │  │
│  └──────────┬───────────────────┘  │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  4. Monta Prompt com         │  │
│  │     Contexto + Pergunta      │  │
│  └──────────┬───────────────────┘  │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  5. Envia para Hugging Face  │  │
│  │     API (LLM Llama-3)        │  │
│  └──────────┬───────────────────┘  │
│             ▼                       │
│  ┌──────────────────────────────┐  │
│  │  6. Retorna Resposta         │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Conta no Hugging Face (gratuita)
- Token de API do Hugging Face

### Passo 1: Instalar Dependências

```powershell
pip install -r requirements.txt
```

### Passo 2: Configurar Token do Hugging Face

1. Acesse [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Crie um novo token de acesso (Read ou Write)
3. Configure a variável de ambiente:

```powershell
$env:HUGGINGFACEHUB_API_TOKEN="seu_token_aqui"
```

Para tornar permanente no Windows, adicione ao perfil do PowerShell ou nas variáveis de ambiente do sistema.

### Passo 3: Executar a Aplicação

```powershell
uvicorn app:app --reload
```

A API estará disponível em: `http://localhost:8000`

## 💻 Como Usar

### Usando a API REST

**Endpoint de Status:**
```bash
GET http://localhost:8000/
```

**Resposta:**
```json
{
  "status": "online",
  "message": "Chatbot DSM API - Use /ask para fazer perguntas"
}
```

**Fazer uma Pergunta:**
```bash
POST http://localhost:8000/ask
Content-Type: application/json

{
  "question": "Qual a duração do curso de DSM?"
}
```

**Resposta:**
```json
{
  "answer": "O curso de Desenvolvimento de Software Multiplataforma (DSM) da Fatec Jacareí tem duração de três anos, divididos em seis semestres."
}
```

### Usando Python

```python
import requests

url = "http://localhost:8000/ask"
payload = {"question": "Quais linguagens são ensinadas no curso?"}

response = requests.post(url, json=payload)
print(response.json()["answer"])
```

### Usando cURL (PowerShell)

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/ask" -Method Post -Body '{"question":"Qual o foco do curso?"}' -ContentType "application/json"
```

### Documentação Interativa

Acesse a documentação automática do Swagger em:
```
http://localhost:8000/docs
```

## 📁 Estrutura do Projeto

```
chatbot/
│
├── app.py                          # Aplicação principal (FastAPI + RAG)
├── requirements.txt                # Dependências do projeto
├── documentacao_chatbot_dsm.md     # Documentação técnica completa
├── gerar_pdf.py                    # Script para gerar PDF da documentação
├── gerar_pdf_simples.py            # Script alternativo de geração de PDF
├── README.md                       # Este arquivo
│
└── __pycache__/                    # Cache do Python (gerado automaticamente)
```

## 🤖 Modelo de Linguagem

### Meta-Llama-3-8B-Instruct

**Características:**
- **Desenvolvedor**: Meta AI
- **Parâmetros**: 8 bilhões
- **Tipo**: Modelo generativo otimizado para instruções
- **Licença**: Gratuita via Hugging Face
- **Endpoint**: `https://router.huggingface.co/v1/chat/completions`

**Justificativa da Escolha:**
- Modelo de alta qualidade disponível gratuitamente via Hugging Face
- Especificamente otimizado para seguir instruções e responder perguntas
- Excelente capacidade de compreensão contextual
- API compatível com padrão OpenAI Chat Completions
- Respostas precisas e determinísticas com temperatura baixa (0.1)
- 8 bilhões de parâmetros garantem qualidade nas respostas

**Configurações Utilizadas:**
- `max_tokens`: 200 (respostas concisas)
- `temperature`: 0.1 (respostas mais determinísticas e precisas)
- `model`: meta-llama/Meta-Llama-3-8B-Instruct

## 🔍 Implementação do RAG

### 1. Base de Conhecimento

O sistema utiliza uma base textual (`knowledge_base`) contendo informações estruturadas sobre:
- Estrutura curricular e duração do curso DSM (3 anos / 6 semestres)
- Disciplinas fundamentais: Lógica de Programação, Banco de Dados, Engenharia de Software
- Linguagens de programação: Python, Java, JavaScript e C#
- Projetos práticos: aplicações móveis, APIs REST, sistemas corporativos, soluções cloud
- Corpo docente qualificado (ex: Professor Marcelo Sudo)
- Requisitos de formatura: estágio supervisionado e Trabalho de Graduação (TG)

### 2. Vetorização (Embeddings)

**Modelo**: `sentence-transformers/all-MiniLM-L6-v2`

**Características:**
- Vetores de 384 dimensões
- Modelo leve e eficiente (apenas 80MB)
- Treinado para capturar similaridade semântica
- Suporta textos em português e inglês

**Processo:**
```python
# 1. Carrega o modelo de embeddings
sentence_encoder = SentenceTransformer(MODEL_EMBEDDING)

# 2. Converte documentos em vetores
vectorized_docs = sentence_encoder.encode(knowledge_base)

# 3. Converte pergunta em vetor (em tempo de execução)
query_vector = sentence_encoder.encode([question])
```

### 3. Indexação e Busca (FAISS)

**FAISS (Facebook AI Similarity Search)**

**Características:**
- Biblioteca otimizada para busca de similaridade vetorial
- Utiliza `IndexFlatL2` (distância euclidiana)
- Busca extremamente rápida mesmo em grandes volumes

**Processo:**
```python
# 1. Cria índice FAISS
vector_dim = 384
vector_index = faiss.IndexFlatL2(vector_dim)

# 2. Adiciona vetores dos documentos
vector_index.add(vectorized_docs.astype('float32'))

# 3. Busca documento mais similar (k=1)
distances, indices = vector_index.search(query_vector, k=1)
relevant_doc = knowledge_base[indices[0][0]]
```

### 4. Geração de Resposta

**Engenharia de Prompt:**

O sistema constrói um prompt estruturado que:
1. Define o papel do assistente (especialista em DSM)
2. Fornece o contexto recuperado como "Texto de Referência"
3. Instrui o modelo a responder apenas com base no contexto fornecido
4. Inclui a pergunta do usuário

```python
system_prompt = f"""
Você é um assistente especializado em responder perguntas sobre o curso de DSM da Fatec Jacareí.
Use exclusivamente o 'Texto de Referência' abaixo para responder.
Se a informação não estiver presente, diga apenas 'Não sei'.

Texto de Referência:
{retrieved_context}

Pergunta: {user_question}
Resposta:
"""
```

### 5. Fluxo Completo

```python
def process_question(request: QuestionRequest):
    # 1. Vetoriza a pergunta
    query_vector = sentence_encoder.encode([request.question])
    
    # 2. Busca contexto relevante no índice
    distances, indices = vector_index.search(query_vector, k=1)
    relevant_doc = knowledge_base[indices[0][0]]
    
    # 3. Gera resposta usando o LLM
    generated_answer = generate_llm_response(relevant_doc, request.question)
    
    # 4. Retorna resposta estruturada
    return QuestionResponse(answer=generated_answer)
```

## ⚠️ Limitações

### 1. Dependência de API Externa
- Requer conexão constante com a internet
- Sujeito a rate limiting do Hugging Face
- Possíveis timeouts ou indisponibilidades

### 2. Configuração Inicial
- Requer token de autenticação válido do Hugging Face
- Variável de ambiente `HUGGINGFACEHUB_API_TOKEN` deve estar configurada
- Aplicação não inicia sem o token configurado

### 3. Base de Conhecimento Restrita
- Apenas um documento sobre o curso DSM
- Não aprende ou atualiza conhecimentos automaticamente
- Perguntas fora do escopo retornam "Não sei"

### 4. Restrições do Modelo
- Limite de 200 tokens pode truncar respostas longas
- Temperatura baixa reduz criatividade
- Possíveis imprecisões mesmo com contexto fornecido

### 5. Escalabilidade
- Índice FAISS mantido em memória RAM
- Sem sistema de cache para respostas repetidas
- Índice recriado a cada reinicialização

### 6. Busca Simplificada
- Recupera apenas 1 documento (k=1)
- Não implementa re-ranking
- Sem histórico de conversação

### 7. Tratamento de Erros
- Tratamento básico de exceções
- Sem sistema de retry automático
- Mensagens de erro podem ser genéricas

## 💬 Exemplo de Uso

### Diálogo Completo (5 Interações)

**1. Pergunta sobre o foco do curso**
```
👤 Usuário: Qual o foco do curso de DSM?

🤖 Chatbot: O principal foco do curso de Desenvolvimento de Software 
Multiplataforma (DSM) da Fatec Jacareí é formar profissionais capazes 
de projetar, desenvolver e manter aplicações modernas para diferentes 
plataformas, como web, dispositivos móveis e desktop, integrando 
sistemas e serviços através de APIs e bancos de dados.
```

**2. Pergunta sobre linguagens de programação**
```
👤 Usuário: Quais linguagens de programação são ensinadas?

🤖 Chatbot: As principais linguagens de programação ensinadas no 
curso de DSM são Python, Java, JavaScript e C#.
```

**3. Pergunta sobre professor específico**
```
👤 Usuário: Quem leciona a matéria de Laboratório de Desenvolvimento Multiplataforma?

🤖 Chatbot: O professor Marcelo Sudo.
```

**4. Pergunta sobre duração**
```
👤 Usuário: Qual a duração do curso?

🤖 Chatbot: O curso de Desenvolvimento de Software Multiplataforma 
(DSM) da Fatec Jacareí tem duração de três anos, divididos em seis 
semestres.
```

**5. Pergunta sobre requisitos de formatura**
```
👤 Usuário: Preciso fazer estágio para me formar?

🤖 Chatbot: Sim, para concluir o curso de Desenvolvimento de Software 
Multiplataforma (DSM) da Fatec Jacareí, é obrigatório realizar um 
estágio supervisionado e apresentar um Trabalho de Graduação (TG).
```

## 📚 Documentação Completa

Para informações técnicas detalhadas, consulte:
- **[documentacao_chatbot_dsm.md](documentacao_chatbot_dsm.md)**: Documentação técnica completa com detalhes sobre implementação, limitações e exemplos

Para gerar a documentação em PDF:
```powershell
python gerar_pdf.py
```

## 🎓 Informações Acadêmicas

**Curso**: Desenvolvimento de Software Multiplataforma (DSM)  
**Instituição**: Fatec Jacareí  
**Disciplina**: Laboratório de Desenvolvimento Multiplataforma  
**Professor**: Marcelo Sudo  

---

**Desenvolvido por**: Murilo  
**Data**: Dezembro de 2025  
**Versão**: 1.0.0
