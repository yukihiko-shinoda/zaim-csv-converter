# @see https://factoryboy.readthedocs.io/en/latest/orms.html#sqlalchemy
import sqlalchemy
from sqlalchemy.orm import scoped_session

from zaimcsvconverter import Session
from zaimcsvconverter.models import initialize_database

CommonSession = scoped_session(Session)


def create_database():
    engine = sqlalchemy.create_engine('sqlite://')
    # It's a scoped_session, and now is the time to configure it.
    CommonSession.configure(bind=engine)
    session = CommonSession()
    initialize_database(engine)

    return session
