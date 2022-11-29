from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserSchema, CreateUserSchema


class UserService:
    """
    User Service
    """
    def get_user(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(db: Session, user: CreateUserSchema):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = User(username=user.username, email=user.email,
                       password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
