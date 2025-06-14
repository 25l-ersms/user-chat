import os
from typing import Any

from google.cloud import firestore  # type: ignore

FIRESTORE_PROJECT_ID = os.getenv("FIRESTORE_PROJECT_ID")
FIRESTORE_DATABASE = os.getenv("FIRESTORE_DATABASE")


def get_client() -> firestore.Client:  # type: ignore
    """
    Get Firestore client.
    Generally firestore depends on enviroment variables to be set.
    """
    return firestore.Client(project=FIRESTORE_PROJECT_ID, database=FIRESTORE_DATABASE)


def add_sample(db: firestore.Client) -> None:  # type: ignore
    """
    Add sample data for test purposes.

    :param db:
    :return:
    """
    doc_ref = db.collection("users").document("user_123")
    doc_ref.set({"name": "Alice", "email": "alice@example.com", "age": 30})


def read_all(db: firestore.Client) -> list[dict[str, Any] | None]:  # type: ignore
    """
    Read all documents from the users collection.
    """
    users_ref = db.collection("users")
    docs = users_ref.stream()
    return [doc.to_dict() for doc in docs]
