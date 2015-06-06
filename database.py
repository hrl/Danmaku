from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import database_settings

engine = create_engine(database_settings["default"],
                       convert_unicode=True,
                       echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_models():
    import models
    session = db_session()
    # test
    user = models.User('1', '1')
    session.add(user)
    session.commit()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    init_models()
