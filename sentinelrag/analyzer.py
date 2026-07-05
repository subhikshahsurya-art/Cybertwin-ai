import chromadb
import json
import subprocess
import os
from chromadb.utils import embedding_functions

VECTORDB_PATH = "/home/subhikshah/Cybertwin/sentinelrag/vectordb"
ALERTS_FILE = "/home/subhikshah/Cybertwin/monitoring/alerts.json"
ANALYSIS_FILE = "/home/subhikshah/Cybertwin/sentinelrag/analysis.json"

client = chromadb.PersistentClient(path=VECTORDB_PATH)
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = client.get_collection(
    name="mitre_attack",
    embedding_function=ef
)

def search_mitre(alert_message):
    results = collection.query(
        query_texts=[alert_message],
        n_results=1
    )
    return {
        'technique': results['metadatas'][0][0]['name'],
        'id': results['metadatas'][0][0]['technique_id']
    }

def ask_ollama(prompt):
    try:
        result = subprocess.run(
            ['ollama', 'run', 'llama3.2', prompt],
            capture_output=True,
            text=True,
            timeout=180
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Analysis timed out"
    except Exception as e:
        return "Error: " + str(e)

def run_analyzer():
    print("SentinelRAG running...")
    try:
        with open(ALERTS_FILE) as f:
            alerts = json.load(f)
    except:
        print("No alerts found")
        return
    analyses = []
    for alert in alerts[-3:]:
        print("Analyzing:", alert['message'])
        mitre = search_mitre(alert['message'])
        prompt = "In 40 words: what is " + alert['message'] + " attack, why dangerous, one action."
        ai_response = ask_ollama(prompt)
        analysis = {
            "alert": alert,
            "mitre_technique": mitre['technique'],
            "mitre_id": mitre['id'],
            "ai_analysis": ai_response
        }
        analyses.append(analysis)
        with open(ANALYSIS_FILE, 'w') as f:
            json.dump(analyses, f, indent=2)
        print("Saved:", alert['message'])
    print("Done. File:", ANALYSIS_FILE)

run_analyzer()
