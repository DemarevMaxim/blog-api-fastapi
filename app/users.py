from sqlalchemy.orm import Session

from app import models, schemas, auth


def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = auth.hash_password(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
