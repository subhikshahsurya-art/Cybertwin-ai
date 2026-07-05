import json
import chromadb
from chromadb.utils import embedding_functions

print("Building vector database...")

client = chromadb.PersistentClient(
    path="/home/subhikshah/Cybertwin/sentinelrag/vectordb"
)

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = client.get_or_create_collection(
    name="mitre_attack",
    embedding_function=ef
)

with open('knowledge/mitre_techniques.json') as f:
    techniques = json.load(f)

docs, ids, metas = [], [], []
for i, t in enumerate(techniques[:200]):
    text = t['name'] + ": " + t['description'] + " Detection: " + t['detection']
    docs.append(text)
    ids.append(str(i))
    metas.append({'technique_id': t['id'], 'name': t['name']})

collection.add(documents=docs, ids=ids, metadatas=metas)
print("Added", len(docs), "techniques to vector database")

