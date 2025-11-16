import schema,utils,database
from fastapi import status,HTTPException,APIRouter
from starlette.responses import Response



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user : schema.UserCreate):

    hpass = utils.hash(user.password)
    user.password = hpass
    database.cursor.execute(""" Insert into users(email, password) values(%s, %s) returning *""",
                   (user.email,user.password))
    user = database.cursor.fetchone()
    print('user is created and added to database')
    database.conn.commit()
    return user

@router.get("/{id}",response_model=schema.UserOut)
def get_user(id: int,response : Response):
    database.cursor.execute(""" Select * from users where id = %s""",(str(id),))
    user = database.cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with {id} is not available')
    return user

