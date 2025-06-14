import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from user_chat.app.routers import messages

# from fastapi.security import OAuth2PasswordBearer


app = FastAPI(
    root_path=os.getenv("USER_CHAT_ROOT_PATH", ""),
)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # TODO setup OAuth and uncomment this line

app.include_router(messages.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
