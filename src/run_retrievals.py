from vector_db import VectorDB

questions = [
    "Quelle est la couleur du chat de Bob ?",
    "Comment s'appelle le chat bleu de Bob ?",
    "Quelle est la couleur du perroquet de Diego ?",
    "Le chat de Bob est vert, non ?",
    "Que fait Gaston quand il pleut ?",
]

db = VectorDB('rag_demo_test')
try:
    for q in questions:
        hits = db.retrieve(q, n=3)
        top = hits[0]['document'] if hits and hits[0]['document'] else ''
        print('Q:', q)
        print('Top-1:', top)
        print()
finally:
    db.close()
