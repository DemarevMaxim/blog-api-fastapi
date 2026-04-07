from sqlalchemy.orm import Session

from app import models, schemas
from app.security import hash_password


# =========================
# USERS
# =========================

def get_user(db: Session, user_id: int):

    return db.query(models.User)\
        .filter(models.User.id == user_id)\
        .first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User)\
        .filter(models.User.email == email)\
        .first()


def get_users(db: Session, skip: int = 0, limit: int = 10):

    return db.query(models.User)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_user(
    db: Session,
    user: schemas.UserCreate
):

    hashed_password = hash_password(
        user.password
    )

    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)

    db.commit()

    db.refresh(db_user)

    return db_user


# =========================
# POSTS
# =========================

def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 10
):

    return db.query(models.Post)\
        .offset(skip)\
        .limit(limit)\
        .all()


def create_user_post(
    db: Session,
    post: schemas.PostCreate,
    user_id: int
):

    db_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=user_id
    )

    db.add(db_post)

    db.commit()

    db.refresh(db_post)

    return db_post
