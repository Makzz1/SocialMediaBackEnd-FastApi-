import schema,utils,database,oauth2
from fastapi import status,HTTPException,APIRouter
from fastapi.params import Depends
from starlette.responses import Response


router = APIRouter(
    prefix="/vote",
    tags= ['Vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote : schema.Vote , curr_user : int = Depends(oauth2.get_current_user)):

    database.cursor.execute("""Select * from posts where id = %s""",(str(vote.post_id),))
    post = database.cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} does not exist")

    database.cursor.execute("""Select * from votes where votes.post_id = %s and votes.user_id = %s""",(str(vote.post_id),str(curr_user['id'])))
    data = database.cursor.fetchone()

    if vote.dir == 1:
        if data :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User {curr_user['email']} has already voted on post {vote.post_id}")
        database.cursor.execute("""Insert into votes (post_id,user_id) values (%s,%s)""""",(str(vote.post_id),str(curr_user['id'])))
        database.conn.commit()
        return {"message":"Successfully added vote"}
    else:
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User {curr_user['email']} has not voted on post {vote.post_id}")
        database.cursor.execute("""Delete from votes where post_id = %s and user_id = %s""",(str(vote.post_id),str(curr_user['id'])))
        database.conn.commit()
        return {"message":"Successfully removed vote"}


