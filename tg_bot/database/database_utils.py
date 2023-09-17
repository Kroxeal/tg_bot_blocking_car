from sqlalchemy.exc import IntegrityError


class DatabaseManager:
    @staticmethod
    def safe_commit(session):
        try:
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            return False
