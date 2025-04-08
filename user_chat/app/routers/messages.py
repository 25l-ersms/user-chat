from typing import Any

from fastapi import APIRouter
from fastapi.params import Depends
from google.cloud import firestore  # type: ignore

from user_chat.firebase_utils.firebase_connector import add_sample, get_client, read_all

router = APIRouter(prefix="/visits", tags=["visits"], responses={404: {"description": "Not found"}})

# TODO probably in real app web sockets will be used? so those endpoints are just for initial testing


@router.get("/send", response_model=None)  # TODO change to real response model and real logic
async def send_a_message(db: firestore.Client = Depends(get_client)) -> None:  # type: ignore
    return add_sample(db)


@router.post("/read", response_model=None)  # TODO change to real response model and real logic
async def read_all_messages(db: firestore.Client = Depends(get_client)) -> list[dict[str, Any] | None]:  # type: ignore
    return read_all(db)
