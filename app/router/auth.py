from logging import raiseExceptions
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import database,schema,utils,oauth2

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login",response_model=schema.Token)
def login(user:OAuth2PasswordRequestForm = Depends()):

    database.cursor.execute("""
    SELECT * FROM users WHERE email = %s
    """,(user.username,))
    data = database.cursor.fetchone()
    # print(data)
    if not data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")

    if not utils.verify(user.password, data['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")

    token = oauth2.create_access_token(data={"user_id":data['id']})

    return {"token": token , "token_type": "bearer"}