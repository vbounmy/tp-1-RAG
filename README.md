# tp-1-RAG

## Objectif
Ce projet implémente une démo RAG minimale :
- brique 1 : base vectorielle persistante avec ChromaDB + sentence-transformers
- brique 3 : orchestration RAG qui récupère des chunks, construit un prompt et appelle un LLM Groq

## Structure du projet
- `src/config.py` : constantes et chemins partagés
- `src/vector_db.py` : classe `VectorDB` pour créer/recharger la base et rechercher des chunks
- `src/rag.py` : classe `RAG` qui orchestre la modération (facultative), le retrieval et l'appel Groq
- `src/main.py` : script de test pour exécuter la brique 3
- `src/test_vector_db.py` : test manuel de la brique 1
- `src/run_retrievals.py` : vérifications de retrieval pour cinq questions
- `data/05_corpus_rag.csv` : corpus de test
- `prompts/rag_system.txt` : prompt système du RAG

## Prérequis
- Python 3.11+ recommandé
- `git` pour gérer les branches
- clé API Groq dans un fichier `.env`

## Installation
1. Crée un environnement virtuel :
```powershell
python -m venv .venv
```
2. Active l'environnement :
```powershell
& .venv\Scripts\Activate.ps1
```
3. Installe les dépendances :
```powershell
pip install -r requirements.txt
```

## Configuration
1. Crée un fichier `.env` à la racine du projet.
2. Ajoute ta clé Groq :
```text
GROQ_API_KEY=ta_cle_api_ici
```
3. Vérifie que `.env` est listé dans `.gitignore`.

## Exécution de la brique 1
Pour vérifier la base vectorielle :
```powershell
& .venv\Scripts\python.exe -m src.test_vector_db
```

## Exécution de la brique 3
Pour tester l'orchestration RAG avec le prompt système et le LLM :
```powershell
& .venv\Scripts\python.exe -m src.main
```

## Vérifications complémentaires
Pour tester le retrieval sur cinq questions et afficher le top-1 :
```powershell
& .venv\Scripts\python.exe -m src.run_retrievals
```

## Conseils de branche
- Crée une branche dédiée pour la partie 6 :
```powershell
git switch -c feature/partie6-test
```

## Notes
- `src/main.py` exécute le pipeline RAG sans modérateur (`use_moderator=False`).
- Pour activer le modérateur, modifie `use_moderator=True` dans `src/main.py`.
- Si le prompt doit être renforcé, le fichier `prompts/rag_system.txt` contient les règles du RAG.
