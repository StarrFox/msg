from fastapi import FastAPI, Security, HTTPException
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials

from msg.security import HashedUsername, HashedPassword
from msg.database import Database, MissingUsername, IncorrectPassword, UsernameInUse
from msg.snowflake import SnowFlakeGenerator

app = FastAPI()
# TODO: replace with real secret key
access_security = JwtAccessBearer(secret_key="b048360d-c702-4197-a073-34b298e2d85d", auto_error=True)
database = Database()
snowflake_gen = SnowFlakeGenerator(machine_id=0)

@app.get("/")
async def root() -> str:
    return "Root"


# TODO: hash password on client
# TODO: restrict what characters can be used
@app.post("/create_user")
async def create_user(username: str, password: str):
    if not 0 < len(username) <= 32:
        raise HTTPException(status_code=401, detail="username must be between 1 and 32 characters")

    if not 0 < len(password) <= 126:
        raise HTTPException(status_code=401, detail="password must be between 1 and 126 characters")

    snowflake = await snowflake_gen.next()

    try:
        await database.create_user(snowflake.value, HashedUsername(username), HashedPassword(password, username))
    except UsernameInUse:
        # TODO: figure out correct status code
        raise HTTPException(status_code=401, detail="username in use")
    
    return snowflake.value


@app.get("/login")
async def login(username: str, password: str):
    try:
        user_id = await database.check_login(HashedUsername(username), HashedPassword(password, username))
    except MissingUsername:
        raise HTTPException(status_code=401, detail="Username not in use")
    except IncorrectPassword:
        raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        user_id = {"user_id": user_id}
        return {"access_token": access_security.create_access_token(subject=user_id)}


@app.post("/messages/{channel_id}")
async def create_message(channel_id: int, user_id: JwtAuthorizationCredentials = Security(access_security)):
    pass


@app.get("/me")
async def me(user_id: JwtAuthorizationCredentials = Security(access_security)) -> int:
    return user_id["user_id"]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
