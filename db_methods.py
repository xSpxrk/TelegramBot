from db_user import User, engine
from sqlalchemy.orm import sessionmaker

maker = sessionmaker(bind=engine)
session = maker()


def is_user_exist(id_user):
    return bool(session.query(User).filter(User.id_user == id_user).scalar())


def add_user(id_user, username, bot, first_name, last_name):
    user = User(id_user=id_user, username=username, bot=bot, first_name=first_name, last_name=last_name)
    session.add(user)
    session.commit()


def get_users_id():
    return [user.id_user for user in session.query(User).all()]


def get_user(id_user):
    return session.query(User).filter(User.id_user == id_user)