import os
import requests
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import faiss

# Configurações do sistema
API_KEY = os.getenv("HUGGINGFACEHUB_API_TOKEN", "").strip()
if not API_KEY:
    raise ValueError("Token de autenticação do Hugging Face não encontrado.")

# Constantes do modelo
MODEL_EMBEDDING = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_LLM = "meta-llama/Meta-Llama-3-8B-Instruct"
API_ENDPOINT = "https://router.huggingface.co/v1/chat/completions"

# Inicializa aplicação FastAPI
app = FastAPI(title="Chatbot RAG - DSM")

# Base de dados de conhecimento
knowledge_base = [
    """O curso de Desenvolvimento de Software Multiplataforma (DSM) da Fatec Jacareí é uma graduação tecnológica com duração de três anos, divididos em seis semestres. 
    O principal foco do curso é formar profissionais capazes de projetar, desenvolver e manter aplicações modernas para diferentes plataformas, como web, dispositivos móveis e desktop, 
    integrando sistemas e serviços através de APIs e bancos de dados.

    Desde o primeiro semestre, os alunos entram em contato com fundamentos sólidos de Lógica de Programação, Banco de Dados e Engenharia de Software, que servem como base para o desenvolvimento das disciplinas seguintes. 
    Ao longo do curso, são trabalhadas diversas linguagens de programação, incluindo Python, Java, JavaScript e C#, além de frameworks e ferramentas que atendem às demandas atuais do mercado de tecnologia.

    Os estudantes têm a oportunidade de desenvolver projetos práticos, como aplicações móveis integradas a APIs REST, sistemas corporativos e soluções baseadas em nuvem. 
    Esses projetos reforçam a experiência prática e o trabalho em equipe, simulando situações reais do ambiente profissional.

    Além da parte técnica, o curso também abrange temas de gestão, análise de sistemas e boas práticas de engenharia de software, preparando o aluno para atuar em diferentes áreas de desenvolvimento e suporte tecnológico. 
    O corpo docente é formado por profissionais qualificados, como o professor Marcelo Sudo, responsável pela disciplina de Laboratório de Desenvolvimento Multiplataforma.

    Para a conclusão do curso, é obrigatório realizar um estágio supervisionado e apresentar um Trabalho de Graduação (TG), o que garante que os alunos passem por experiências práticas antes da formatura. 
    Dessa forma, o curso DSM forma profissionais preparados para ingressar no mercado de trabalho com uma visão ampla e atualizada do desenvolvimento de software."""
]

# Inicialização do sistema RAG
print("[INFO] Iniciando carregamento do modelo de embeddings...")
sentence_encoder = SentenceTransformer(MODEL_EMBEDDING)

print("[INFO] Processando documentos da base de conhecimento...")
vectorized_docs = sentence_encoder.encode(knowledge_base)

print("[INFO] Construindo índice vetorial FAISS...")
vector_dim = vectorized_docs.shape[1]
vector_index = faiss.IndexFlatL2(vector_dim)
vector_index.add(vectorized_docs.astype('float32'))
print("[INFO] Sistema RAG inicializado com sucesso.")

# Funções auxiliares do sistema
def generate_llm_response(retrieved_context: str, user_question: str) -> str:
    """Gera resposta usando o LLM do Hugging Face com contexto recuperado."""
    auth_headers = {"Authorization": f"Bearer {API_KEY}"}
    
    system_prompt = (
        "Você é um assistente especializado em responder perguntas sobre o curso de Desenvolvimento de Software Multiplataforma (DSM) da Fatec Jacareí. "
        "Use exclusivamente o 'Texto de Referência' abaixo para responder. "
        "Se a informação não estiver presente, diga apenas 'Não sei'.\n\n"
        f"Texto de Referência:\n{retrieved_context}\n\n"
        f"Pergunta: {user_question}\nResposta:"
    )

    request_body = {
        "model": MODEL_LLM,
        "messages": [
            {"role": "user", "content": system_prompt}
        ],
        "max_tokens": 200,
        "temperature": 0.1
    }

    try:
        api_response = requests.post(API_ENDPOINT, headers=auth_headers, json=request_body)
        api_response.raise_for_status()
        response_data = api_response.json()
        if not response_data["choices"] or not response_data["choices"][0]["message"]["content"]:
            return "Não sei."
        return response_data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as http_err:
        error_msg = http_err.response.text
        print(f"[ERRO] Falha na API ({http_err.response.status_code}): {error_msg}")
        raise HTTPException(status_code=http_err.response.status_code, detail=error_msg)
    except Exception as generic_err:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {generic_err}")

# Modelos de dados para requisições e respostas
class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

# Endpoints da API REST
@app.post("/ask", response_model=QuestionResponse)
def process_question(request: QuestionRequest):
    """Endpoint principal: processa pergunta usando RAG e retorna resposta do LLM."""
    query_vector = sentence_encoder.encode([request.question]).astype('float32')
    
    distances, indices = vector_index.search(query_vector, k=1)
    
    if not indices.size > 0:
        return QuestionResponse(answer="Não sei.")

    relevant_doc = knowledge_base[indices[0][0]]
    
    print("[DEBUG] Documento recuperado do índice")
    print(f"[DEBUG] Contexto (preview): {relevant_doc[:300]}...")
    print("[DEBUG] Enviando para LLM...")
    
    generated_answer = generate_llm_response(relevant_doc, request.question)
    
    return QuestionResponse(answer=generated_answer)

@app.get("/")
def health_check():
    return {"status": "online", "message": "Chatbot DSM API - Use /ask para fazer perguntas"}}
