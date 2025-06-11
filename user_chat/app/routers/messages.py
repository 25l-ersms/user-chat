import os
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Header, WebSocket, WebSocketDisconnect
from google.cloud import firestore  # type: ignore
from jose import jwt, JWTError, ExpiredSignatureError

from user_chat.firebase_utils.firebase_connector import add_sample, get_client, read_all, send_message, get_messages
from user_chat.app.models.models import MessageModel

router = APIRouter(prefix="/visits", tags=["visits"], responses={404: {"description": "Not found"}})

# Secret key and algorithm for JWT
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"


def decode_jwt(token: str) -> dict:
    """
    Decode the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# TODO probably in real app web sockets will be used? so those endpoints are just for initial testing


#@router.get("/send", response_model=None)  # TODO change to real response model and real logic
#async def send_a_message(db: firestore.Client = Depends(get_client)) -> None:  # type: ignore
#    return add_sample(db)


#@router.post("/read", response_model=None)  # TODO change to real response model and real logic
#async def read_all_messages(db: firestore.Client = Depends(get_client)) -> list[dict[str, Any] | None]:  # type: ignore
#    return read_all(db)


@router.post("/send", response_model=None)
async def send_message_endpoint(
    message: MessageModel, authorization: str = Header(...), db: firestore.Client = Depends(get_client)
) -> None:
    """
    Send a message after decoding the JWT token to verify the sender.
    """
    # Extract and decode the JWT token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please login again.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Extract user_id from the token payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Verify that the sender_id matches the user_id from the token
    if message.sender_id != user_id:
        raise HTTPException(status_code=403, detail="Sender ID does not match the authenticated user")

    # Send the message
    send_message(db, message.dict())

    # Broadcast the message to all connected WebSocket clients
    for client in connected_clients:
        await client.send_json(message.dict())


#@router.get("/messages/{user_id}", response_model=list[MessageModel])
#async def get_messages_endpoint(user_id: str, db: firestore.Client = Depends(get_client)) -> list[dict]:
#    return get_messages(db, user_id)


@router.get("/messages", response_model=list[MessageModel])
async def get_messages_endpoint(
    authorization: str = Header(...), db: firestore.Client = Depends(get_client)
) -> list[dict]:
    """
    Retrieve all messages where the user is either the sender or receiver based on the JWT token.
    """
    # Extract and decode the JWT token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = authorization.split("Bearer ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired. Please login again.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Extract user_id from the token payload
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Fetch messages where user_id is either sender or receiver
    messages_ref = db.collection("messages").where("sender_id", "==", user_id).stream()
    received_messages_ref = db.collection("messages").where("receiver_id", "==", user_id).stream()

    # Combine and return messages
    sent_messages = [doc.to_dict() for doc in messages_ref]
    received_messages = [doc.to_dict() for doc in received_messages_ref]
    return sent_messages + received_messages

# Store connected clients
connected_clients = []

@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat updates.
    """
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            # Wait for messages from the client (optional)
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
