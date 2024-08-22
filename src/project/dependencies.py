from collections.abc import Generator

from sqlalchemy import exc
from sqlalchemy.orm import Session, sessionmaker

from .database import engine


def get_db_session() -> Generator[Session, None, None]:
    factory = sessionmaker(engine)
    with factory() as session:
        try:
            yield session
            session.commit()
        except exc.SQLAlchemyError as error:
            session.rollback()
            raise error
        except Exception as error:
            session.rollback()
            raise error
        finally:
            session.close()
