from vector_db import VectorDB


def main():
    print('Démarrage du test VectorDB')
    db = VectorDB('rag_demo_test')
    try:
        print('Collection name:', db.collection.name)
        try:
            print('Count:', db.collection.count())
            print('Peek:', db.collection.peek(5))
        except Exception as e:
            print('Info collection error:', e)
        hits = db.retrieve('Quelle est la couleur du chat de Bob ?', n=3)
        print('Résultats:')
        for h in hits:
            print(h)
    finally:
        db.close()


if __name__ == '__main__':
    main()
