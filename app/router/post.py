import schema
from fastapi import status,HTTPException,APIRouter,Depends
from starlette.responses import Response
from typing import List
import database,oauth2


router = APIRouter(
    prefix = "/posts",
    tags = ['Posts']
)


@router.get("/",response_model=List[schema.VotePostResponse])
def get_posts(cur_user : int = Depends(oauth2.get_current_user),
              limit : int = 10):
    print(limit)
    print(cur_user)
    database.cursor.execute(""" Select posts.*,count(votes.post_id) as vote 
                                from Posts left join votes 
                                on posts.id = votes.post_id 
                                where posts.user_id = %s 
                                group by posts.id
                                limit %s """,
                            (str(cur_user['id']),str(limit)))
    my_posts = database.cursor.fetchall()
    return my_posts

@router.post("/",status_code=status.HTTP_201_CREATED ,
             response_model=schema.PostResponse)
def create_posts(post : schema.PostCreate,
                 cur_user : int = Depends(oauth2.get_current_user)):
    # post = post.dict()
    # print('Post is created')
    # global id
    # post['id'] = id
    # id += 1
    # my_posts.append(post)
    database.cursor.execute(""" Insert into posts(title, content, user_id) values(%s, %s, %s)  returning *""",
                   (post.title,post.content,cur_user['id']))
    post = database.cursor.fetchone()
    print('post is created and added to database')
    database.conn.commit()
    return post

@router.get("/{id}",response_model=schema.PostResponse)
def get_post(id: int,response : Response,
             cur_user : int = Depends(oauth2.get_current_user)):
    # for i in my_posts:
    #     if i["id"] == id:
    #         return {"post":i}
    #
    # # response.status_code = status.HTTP_404_NOT_FOUND
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} is not available')
    database.cursor.execute(""" Select * from posts where id = %s""",(str(id),))
    post = database.cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with {id} is not available')
    return post
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,
                cur_user : int = Depends(oauth2.get_current_user)):
    # for i in my_posts:
    #     if i["id"] == id:
    #         my_posts.remove(i)
    #         return Response(status_code=status.HTTP_204_NO_CONTENT)
    #
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {id} is not available')
    database.cursor.execute(""" delete from posts where id = %s returning *""",
                   (str(id),))
    post = database.cursor.fetchone()
    database.conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {id} is not available')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schema.PostResponse)
def update(id : int,post : schema.PostCreate,
           cur_user : int = Depends(oauth2.get_current_user)):
    # post = post.dict()
    # post['id'] = id
    # for i in my_posts:
    #     if i['id'] == id:
    #         my_posts.remove(i)
    #         my_posts.append(post)
    #         return {'msg':'updated'}
    #
    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with {id} is not available')
    database.cursor.execute(
        """Update posts 
        set title = %s , 
        content = %s,
        published = %s
        where id = %s 
        returning *""",
                   (post.title,post.content,post.published,str(id)))
    post = database.cursor.fetchone()
    database.conn.commit()
    if post:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with {id} is not available')
