from sqlalchemy import Column, Integer, String, BigInteger, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.db')

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, nullable=False)
    username = Column(String)
    bot = Column(Boolean, nullable=False)
    first_name = Column(String)
    last_name = Column(String)


Base.metadata.create_all(engine)
