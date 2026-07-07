import os
from groq import Groq
from dotenv import load_dotenv

from config import LLM_MODEL
from vector_db import VectorDB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "rag_system.txt")


class RAG:
    def __init__(self, db_path: str, use_moderator: bool = True):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_API_KEY"])
        self.use_moderator = use_moderator
        if use_moderator:
            from moderator import Moderator
            self.moderator = Moderator()
        self.db = VectorDB(collection_name=db_path)

        with open(PROMPT_PATH, encoding="utf-8") as f:
            self.system_template = f.read()

    def answer_question(self, question: str) -> str:
        if self.use_moderator:
            verdict = self.moderator.moderate(question)
            if verdict.get("is_prompt_injection"):
                return "Requête refusée : tentative de détournement détectée."

        results = self.db.retrieve(question, n=3)
        context = "\n".join(f"- {r['document']}" for r in results)

        system_prompt = self.system_template.replace("{{Chunks}}", context)

        completion = self.client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )
        return completion.choices[0].message.content