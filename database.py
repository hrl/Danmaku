import json

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
    # user
    user = models.User('1', '1')
    session.add(user)
    session.commit()
    # danmaku
    danmaku = models.Danmaku("Danmaku Pool A")
    session.add(danmaku)
    session.commit()
    # tsukkomi
    tsukkomi_with_user = models.Tsukkomi(
        danmaku=danmaku,
        body="丢锅啦",
        style={
            "color": "FFF",
        },
        start_time=1,
        spoiler=False,
        owner=user,
    )
    session.add(tsukkomi_with_user)
    session.commit()

    tsukkomi_without_user = models.Tsukkomi(
        danmaku=danmaku,
        body="这个人是凶手(",
        style=json.dumps({
            "color": "FFF",
        }),
        start_time=1,
        spoiler=True,
    )
    session.add(tsukkomi_without_user)
    session.commit()
    # file
    file_0 = models.File("8f60c8102d29fcd525162d02eed4566b", danmaku)
    session.add(file_0)
    session.commit()
    # youku video
    youku_video = models.YoukuVideo("313877787", "XMTI1NTUxMTE0OA==", danmaku)
    session.add(youku_video)
    session.commit()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    init_models()
