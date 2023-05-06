from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


app = FastAPI()


class User(BaseModel):
    username: str
    nickname: str


@app.get("/")
async def root() -> str:
    return "Root"


@app.post("/messages/{channel_id}")
async def create_message(channel_id: int):
    pass


def decode_token(token: str) -> User:
    return User(
        username="test",
        nickname="testnick"
    )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return decode_token(token)


@app.get("/me")
async def me(me: Annotated[User, Depends(get_current_user)]) -> User:
    return me


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
