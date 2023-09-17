import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, Boolean, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, relationship

from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


host = str(os.environ.get('HOST'))
password = str(os.environ.get('PASSWORD'))
database = str(os.environ.get('DATABASE'))
username = str(os.environ.get('USERNAME_TG'))
port = str(os.environ.get('PORT'))

engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

user_car_association = Table(
    'user_car_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('car_id', Integer, ForeignKey('cars.id')),
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(40))
    first_name = Column(String(20))
    last_name = Column(String(20))
    phone_number = Column(String, nullable=True)
    registration_date = Column(DateTime(), default=datetime.now)
    isAdmin = Column(Boolean, default=False)

    cars = relationship('Car', secondary=user_car_association, back_populates='users')


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=Table)
    brand_car = Column(String(30))
    model_car = Column(String(30))
    year = Column(Integer)
    license_plate = Column(String(10))
    color = Column(String(10))

    users = relationship('User', secondary=user_car_association, back_populates='cars')


Base.metadata.create_all(bind=engine)
