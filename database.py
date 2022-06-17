from sqlalchemy.orm import Session
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy.orm import declarative_base
import secrets
from email_script import send_email

Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"
    discord_id = Column(Integer, primary_key=True)
    email = Column(String)
    token = Column(String)
    verified = Column(Boolean)

    def __repr__(self):
        return f"User(email={self.email!r}, discord_id={self.discord_id!r}, token={self.token!r}, verified={self.verified!r})"


engine = db.create_engine(
    "postgresql://ndjqgujmuroukk:1620275244fa767a6a29241d81159ab9a9a04e50ecdb3a8007b386aedcae693b@ec2-54-147-33-38.compute-1.amazonaws.com:5432/d1fm818lms9gef")


def check_email(email):
    with Session(engine) as session:
        stmt = select(User).where(User.email.in_([email]))
        if session.scalars(stmt).first():
            return True
        else:
            return False


def gen_token(email):
    with Session(engine) as session:
        stmt = select(User).where(User.email.in_([email]))
        user = session.scalars(stmt).first()
        token = secrets.token_urlsafe(32)
        send_email(email, token)
        user.token = token
        session.commit()


def save_discord_id(email, discord_id):
    with Session(engine) as session:
        stmt = select(User).where(User.email.in_([email]))
        user = session.scalars(stmt).first()
        user.discord_id = discord_id
        session.commit()


def check_token(discord_id, token):
    with Session(engine) as session:
        user = session.get(User, str(discord_id))
        if user.token == token:
            return True
        else:
            return False


def set_verify(discord_id):
    with Session(engine) as session:
        user = session.get(User, str(discord_id))
        user.verified = True
        session.commit()


def check_verify(email):
    with Session(engine) as session:
        stmt = select(User).where(User.email.in_([email]))
        user = session.scalars(stmt).first()
        return user.verified


# ========================== testing functions =============================

def add_user(email):
    with Session(engine) as session:
        user = User(email=email, verified=False)
        session.add(user)
        session.commit()


def del_user(email):
    with Session(engine) as session:
        stmt = select(User).where(User.email.in_([email]))
        user = session.scalars(stmt).first()
        session.delete(user)
        session.commit()
