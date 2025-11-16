from jose import JWTError, jwt
from datetime import datetime, timedelta
import schema,database
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data : dict):
    to_enocde = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_enocde.update({"exp": expire})

    token = jwt.encode(
        to_enocde,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


    token = verify_token(token, credential_exception)
    database.cursor.execute("SELECT * FROM users WHERE id = %s", (token.id,))

    user = database.cursor.fetchone()

    return user