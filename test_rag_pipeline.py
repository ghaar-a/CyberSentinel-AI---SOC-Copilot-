import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

# 1. Configuração Inicial
print("🔄 Carregando modelo SentenceTransformers (isso pode levar alguns segundos na primeira vez)...")
# Usando um modelo super rápido e eficiente para CPU
model = SentenceTransformer('all-MiniLM-L6-v2') 

def load_and_chunk_markdown(directory_path, chunk_size=500):
    """Simula o KnowledgeLoader e o MarkdownChunker"""
    chunks = []
    print(f"\n📂 Lendo arquivos da pasta: {directory_path}")
    
    path = Path(directory_path)
    if not path.exists():
        print(f"❌ Erro: A pasta {directory_path} não existe.")
        return chunks

    for filepath in path.glob("*.md"):
        print(f"  📄 Lendo: {filepath.name}")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Fatiamento simplificado por blocos de texto (simulando seu chunker)
            paragraphs = content.split('\n\n')
            
            current_chunk = ""
            for p in paragraphs:
                if len(current_chunk) + len(p) < chunk_size:
                    current_chunk += p + "\n\n"
                else:
                    if current_chunk.strip():
                        chunks.append({"text": current_chunk.strip(), "source": filepath.name})
                    current_chunk = p + "\n\n"
            if current_chunk.strip():
                 chunks.append({"text": current_chunk.strip(), "source": filepath.name})
                 
    return chunks

# 2. Carregar e Fatiar os Documentos
docs_path = "./docs" # Apontando para a pasta que já tem conteúdo
document_chunks = load_and_chunk_markdown(docs_path)

print(f"\n✅ Total de chunks gerados: {len(document_chunks)}")

# 3. Gerar Embeddings (Indexação In-Memory)
print("\n🧠 Gerando embeddings para os chunks...")
texts = [chunk["text"] for chunk in document_chunks]
# Converte a lista de textos em uma matriz matemática
document_embeddings = model.encode(texts, convert_to_tensor=True)
print(f"✅ Embeddings gerados! Dimensão do vetor: {document_embeddings.shape}")

# 4. Fazer uma Consulta Semântica Real
query = "Quais são as limitações do assistente e o que ele não deve fazer?"
print(f"\n🔎 Testando consulta: '{query}'")

# Converte a pergunta em vetor
query_embedding = model.encode(query, convert_to_tensor=True)

# 5. Calcular a similaridade (Cosine Similarity)
from sentence_transformers import util
hits = util.semantic_search(query_embedding, document_embeddings, top_k=3)[0]

# 6. Exibir os Resultados
print("\n🏆 Top 3 Resultados Encontrados:\n")
for i, hit in enumerate(hits):
    score = hit['score']
    chunk_id = hit['corpus_id']
    source = document_chunks[chunk_id]['source']
    text = document_chunks[chunk_id]['text'][:200] + "..." # Mostra só os primeiros 200 caracteres
    
    print(f"--- Resultado {i+1} ---")
    print(f"📂 Arquivo: {source}")
    print(f"🎯 Score (Similaridade): {score:.4f}")
    print(f"📝 Trecho: {text}\n")