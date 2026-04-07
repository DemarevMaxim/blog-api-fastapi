from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app import models, schemas, crud

# создаём таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Blog API is running"}


# =========================
# USERS
# =========================

# регистрация пользователя
@app.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    db_user = crud.get_user_by_email(
        db,
        email=user.email
    )

    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return crud.create_user(
        db=db,
        user=user
    )


# получение пользователей
@app.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    users = crud.get_users(
        db,
        skip=skip,
        limit=limit
    )

    return users


# =========================
# POSTS
# =========================

# создание поста
@app.post(
    "/users/{user_id}/posts/",
    response_model=schemas.Post
)
def create_post_for_user(
    user_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user_post(
        db=db,
        post=post,
        user_id=user_id
    )


# получение постов
@app.get(
    "/posts/",
    response_model=list[schemas.Post]
)
def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    posts = crud.get_posts(
        db=db,
        skip=skip,
        limit=limit
    )

    return posts

# =========================
# POSTS
# =========================

@app.get(
    "/posts/",
    response_model=list[schemas.Post]
)
def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    posts = crud.get_posts(
        db,
        skip=skip,
        limit=limit
    )

    return posts


@app.post(
    "/users/{user_id}/posts/",
    response_model=schemas.Post
)
def create_post_for_user(
    user_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user_post(
        db=db,
        post=post,
        user_id=user_id
    )



