from fastapi import FastAPI
from router import post,user,auth,vote
import database
from fastapi.middleware.cors import CORSMiddleware

orgins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def hello():
    print('test')
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.on_event("startup")
def startup():
    database.startup()

@app.on_event("shutdown")
def shutdown():
    database.shutdown()



