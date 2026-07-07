from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List, Optional

from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

from config import CHROMA_PERSIST_PATH, CORPUS_CSV_PATH, EMBEDDING_MODEL


class VectorDB:
    def __init__(self, collection_name: str, chunks: Optional[List[Dict[str, str]]] = None) -> None:
        self.client = PersistentClient(path=str(Path(CHROMA_PERSIST_PATH)))
        self.collection_name = collection_name

        # Si la collection existe déjà, la charger et l'utiliser dans le modèle
        existing_names = [collection.name for collection in self.client.list_collections()]
        if collection_name in existing_names:
            self.collection = self.client.get_collection(collection_name)
            model_name = self.collection.metadata.get("embedding_model", EMBEDDING_MODEL)
            self.model = SentenceTransformer(model_name)
            # Si la collection existe mais est vide, essayer d'indexer à partir du CSV ou des chunks fournis
            try:
                if self.collection.count() == 0:
                    chunks_to_index = chunks or self._load_csv_chunks()
                    if chunks_to_index:
                        self._index_chunks(self.collection, chunks_to_index)
            except Exception:
                # Non-fatal: continuer même si count/peek n'est pas supporté
                pass
        else:
            # Pour une nouvelle collection, préparer le modèle (à partir de la configuration) avant l'indexation
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            self.collection = self._get_or_create_collection(chunks or self._load_csv_chunks())

    def _load_csv_chunks(self) -> List[Dict[str, str]]:
        if not CORPUS_CSV_PATH.exists():
            return []

        with CORPUS_CSV_PATH.open(newline="", encoding="utf-8") as csvfile:
            return [row for row in csv.DictReader(csvfile)]

    def _get_or_create_collection(self, chunks: List[Dict[str, str]]) -> Any:
        existing_names = [collection.name for collection in self.client.list_collections()]
        if self.collection_name in existing_names:
            return self.client.get_collection(self.collection_name)

        if not chunks:
            raise ValueError("Aucune collection existante et aucun chunk fourni.")

        collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"embedding_model": EMBEDDING_MODEL},
        )
        self._index_chunks(collection, chunks)
        return collection

    def _index_chunks(self, collection: Any, chunks: List[Dict[str, str]]) -> None:
        documents = [chunk["text"] for chunk in chunks]
        ids = [chunk.get("id", f"chunk-{i}") for i, chunk in enumerate(chunks)]
        metadatas = [
            {"source": chunk.get("source", ""), "categorie": chunk.get("categorie", "")}
            for chunk in chunks
        ]
        embeddings = self.model.encode(
            documents,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)

    def retrieve(self, question: str, n: int = 3) -> List[Dict[str, Any]]:
        if not question:
            raise ValueError("La question ne peut pas être vide.")

        embedding = self.model.encode(
            [question],
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]
        result = self.collection.query(
            query_embeddings=[embedding],
            n_results=n,
            include=["documents", "metadatas", "distances"],
        )
        return [
            {"document": doc, "metadata": meta, "distance": dist}
            for doc, meta, dist in zip(
                result.get("documents", []),
                result.get("metadatas", []),
                result.get("distances", []),
            )
        ]

    def close(self) -> None:
        self.client.close()
