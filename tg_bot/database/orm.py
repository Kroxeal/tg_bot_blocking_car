from aiogram import types
from sqlalchemy.orm import joinedload

from tg_bot_aiogram.tg_bot.database.settings import User, session, Car

from tg_bot_aiogram.tg_bot.database.database_utils import DatabaseManager


class Registration:
    @staticmethod
    def registration_user(
        message,
        first_name,
        last_name,
        phone_number,
    ):
        new_user = User(
            id=int(message.from_user.id),
            username=message.from_user.username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        session.add(new_user)

        DatabaseManager.safe_commit(session)

    @staticmethod
    def registration_car(
        brand_car,
        model_car,
        year,
        license_plate,
        color,
    ):
        new_car = Car(
            brand_car=brand_car,
            model_car=model_car,
            year=year,
            license_plate=license_plate,
            color=color,
        )

        session.add(new_car)

        DatabaseManager.safe_commit(session)

    @staticmethod
    def add_car_to_user(
        user_id,
        brand_car,
        model_car,
        year,
        license_plate,
        color,
    ):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            new_car = Car(
                brand_car=brand_car,
                model_car=model_car,
                year=year,
                license_plate=license_plate,
                color=color,
            )
            user.cars.append(new_car)
            DatabaseManager.safe_commit(session)
        else:
            print(f"Пользователь с id {user_id} не найден.")


class UserManager:
    @staticmethod
    def is_username_exists(username: str, session) -> bool:
        try:
            user = session.query(User).filter_by(username=username).first()
            return True if user else False
        except Exception as e:
            print(f"Error {e}")
            return False
        finally:
            session.close()

    @staticmethod
    def get_user_id(message: types.Message):
        return message.from_user.id


class CarManager:
    @staticmethod
    def get_users_by_license_plate(license_plate):
        try:
            car = session.query(Car).filter_by(license_plate=license_plate).options(joinedload(Car.users)).first()
            if car:
                owners = car.users
                return owners
            else:
                return None
        except Exception as e:
            print(f'Error: {e}')
            return None

    @staticmethod
    def get_car_info(username):
        try:
            user = session.query(User).filter_by(username=username).first()
            if user:
                cars = user.cars
                car_info = []
                for car in cars:
                    car_info.append((car.brand_car, car.license_plate))
                return car_info
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            session.close()

