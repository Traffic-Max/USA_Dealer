# bot_service/models.py

from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config


DATABASE_URL = 'postgresql://mg_admin:2517@localhost/mg_db'

# Инициализация SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# здесь определяются все операции с базой данных
class DBConnectionError(Exception):
    pass


def check_db_connection():
    try:
        engine = create_engine('postgresql://mg_admin:2517@localhost/mg_db')
        connection = engine.connect()
    except Exception as e:
        raise DBConnectionError("[!] Не удалось подключиться к базе данных: " + str(e))
    else:
        connection.close()


def create_tables():
    Base.metadata.create_all(engine)

def drop_tables():
    Base.metadata.drop_all(engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    user_firstname = Column(String)
    username = Column(String, unique=True)
    status = Column(String, default="empty")

def register_user(user_id, username, firstname):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(user_id=user_id, username=username, user_firstname=firstname, status="admin" if user_id == config.ROOT_ADMIN_ID else "user")
            session.add(user)
            session.commit()
            print(f"User {user.username} with ID {user.user_id} with status {user.status} registered succesfully!")
        else:
            print(f"User {user.username} with ID {user.user_id} already registered.")
    finally:
        session.close()
    return user


class AdminApplication(Base):
    __tablename__ = "admin_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    username = Column(String)
    status = Column(String, default="pending")

def apply_for_admin(user_id, firstname):
    session = SessionLocal()
    try:
        application = AdminApplication(user_id=user_id, username=firstname)
        session.add(application)
        session.commit()
    finally:
        session.close()


# Создание модели для постов
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    description = Column(String)
    approved = Column(Boolean, default=False)


def add_content_to_db(content, description):
    session = SessionLocal()
    try:
        post = Post(content=content, description=description)
        session.add(post)
        session.commit()
    except SQLAlchemyError as e:
        print("[!] Произошла ошибка при добавлении в базу данных: " + str(e))
        return False
    finally:
        session.close()
    return True

"""
Обратите внимание, что эти функции создают или удаляют все таблицы,
которые определены в вашем Base классе.
Если вы хотите создать или удалить конкретную таблицу, 
вы можете использовать метод create() или drop() класса Table:

Post.__table__.create(engine)
Post.__table__.drop(engine)

"""