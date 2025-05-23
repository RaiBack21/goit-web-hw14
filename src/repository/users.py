import redis.asyncio as redis
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.conf.config import settings


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user with the specified email.
    
    :param email: The email of user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with specified email, or None if it does not exist.
    :rtype: User | None
    """
    return db.query(User).filter(User.email == email).first() 


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    new_user = User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates a token for a specific user.

    :param token: The token to update.
    :type token: str | None
    :param user: The user to update the token for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    Update email confirmation field.

    :param email: The email of the user to confirm.
    :type email: int
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_password(user: User, password: str, db: Session) -> None:
    """
    Updates a password for a specific user.

    :param password: The new password to update.
    :type password: str
    :param user: The user to update the password for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: None.
    :rtype: None
    """
    user.password = password
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates avatar for a specific user.

    :param email: The email of the user to update.
    :type email: str
    :param url: The url of new avatar.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated user, or None if it does not exist.
    :rtype: User | None
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
