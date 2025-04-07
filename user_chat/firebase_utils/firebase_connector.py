from typing import Any

from google.cloud import firestore


def get_client() -> firestore.Client:
    """
    Get Firestore client.
    Generally firestore depends on enviroment variables to be set.
    """
    return firestore.Client(project="demo-project")

def add_sample(db: firestore.Client) -> None:
    """
    Add sample data for test purposes.

    :param db:
    :return:
    """
    doc_ref = db.collection("users").document("user_123")
    doc_ref.set({
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30
    })

def read_all(db: firestore.Client) -> list[dict[str, Any] | None]:
    """
    Read all documents from the users collection.
    """
    users_ref = db.collection("users")
    docs = users_ref.stream()
    return [doc.to_dict() for doc in docs]
