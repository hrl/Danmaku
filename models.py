import uuid
import json

from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.schema import (
    UniqueConstraint,
    PrimaryKeyConstraint,
    Index,
)

from sqlalchemy import (
    Table,
    Column,
    Integer,
    BigInteger,
    Unicode,
    UnicodeText,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    relationship,
    backref,
)

from database import Base
import util


class GUID(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class User(Base):
    __tablename__ = 'user'
    id = Column(GUID(),
                default=uuid.uuid4,
                primary_key=True)
    username = Column(Unicode(20),
                      unique=True,
                      nullable=True)
    password = Column(Unicode(100),
                      nullable=True)
    create_time = Column(DateTime(timezone=True),
                         nullable=False)

    def __init__(self, username=None, password=None,
                 permissions=(),
                 create_time=None):
        timenow = util.get_utc_time()
        if create_time is None:
            create_time = timenow
        self.username = username
        if password is not None:
            self.set_password(password)
        self.create_time = create_time
        for permission in permissions:
            self.permissions.append(permission)

    def __repr__(self):
        return "<User: %s>" % self.username

    def check_password(self, request_pwd):
        return util.check_password(request_pwd, self.password)

    def set_password(self, new_pwd):
        self.password = util.set_password(new_pwd)

    def format_detail(self, call_by_admin=False):
        detail = {
            "uuid": self.id.hex,
            "username": self.username,
        }
        return detail

    @property
    def permission_list(self):
        permissions = []
        for permission in self.permissions:
            permissions.append((permission.name, permission.perm))
        return permissions


user_permission_table = Table('user_permission', Base.metadata,
                              Column('user_id',
                                     GUID(), ForeignKey('user.id')),
                              Column('permission_id',
                                     GUID(), ForeignKey('permission.id')))


class Permission(Base):
    __tablename__ = 'permission'
    __table_args__ = (
        Index('_name_perm_idx', 'name', 'perm', unique=True),
    )
    id = Column(GUID(),
                default=uuid.uuid4,
                primary_key=True)
    # permisson name, eg: reply
    name = Column(Unicode(20),
                  nullable=False)
    # permisson type, eg: read
    perm = Column(Unicode(20),
                  nullable=False)
    users = relationship("User",
                         secondary=user_permission_table,
                         backref=backref("permissions",
                                         lazy="subquery"),
                         lazy="dynamic")

    def __init__(self, name, perm):
        self.name = name
        self.perm = perm

    def __repr__(self):
        return "<Permission: %s, %s>" % (self.name, self.perm)

    def format_detail(self):
        detail = {
            "uuid": self.id.hex,
            "name": self.name,
            "perm": self.perm
        }
        return detail


class Danmaku(Base):
    __tablename__ = 'danmaku'
    id = Column(GUID(),
                default=uuid.uuid4,
                primary_key=True)
    name = Column(Unicode(20),
                  nullable=False)
    tsukkomi = relationship("Tsukkomi",
                            backref=backref("danmaku",
                                            lazy="noload"),
                            cascade="all, delete-orphan",
                            lazy="dynamic")
    create_time = Column(DateTime(timezone=True),
                         nullable=False)

    def __init__(self, name,
                 create_time=None):
        timenow = util.get_utc_time()
        if create_time is None:
            create_time = timenow
        self.name = name
        self.create_time = create_time

    def __repr__(self):
        return "<Danmaku: %s>" % (self.name)

    def format_detail(self):
        detail = {
            "uuid": self.id.hex,
            "name": self.name,
            "create_time": self.create_time.isoformat(),
        }
        return detail


class Tsukkomi(Base):
    __tablename__ = 'tsukkomi'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'danmaku_id', name='tsukkomi_danmaku_pk'),
    )
    id = Column(Integer, index=True)
    danmaku_id = Column(GUID(), ForeignKey('danmaku.id'), index=True)

    owner_id = Column(GUID(), ForeignKey('user.id'), nullable=True)
    owner = relationship("User",
                         backref=backref("tsukkomi",
                                         lazy="dynamic",
                                         cascade="all"),
                         lazy="subquery")

    body = Column(UnicodeText(),
                  nullable=False)
    spoiler = Column(Boolean,
                     default=False,
                     nullable=False)
    style = Column(UnicodeText(),
                   nullable=False)
    # s
    start_time = Column(Integer,
                        nullable=False)
    source = Column(UnicodeText(100),
                    nullable=True)
    create_time = Column(DateTime(timezone=True),
                         nullable=False)

    def __init__(self, danmaku, body, style, start_time,
                 spoiler=False, owner=None,
                 create_time=None, id=None):
        timenow = util.get_utc_time()
        if create_time is None:
            create_time = timenow
        if id is None:
            id = danmaku.tsukkomi.count() + 1
        if spoiler:
            spoiler = True
        else:
            spoiler = False
        self.id = id
        self.danmaku = danmaku
        self.owner = owner
        self.body = body
        self.spoiler = spoiler
        self.style = json.dumps(style)
        self.start_time = start_time
        self.create_time = create_time

    def __repr__(self):
        return "<Tsukkomi: %s, %d, %s>" % (self.danmaku_id.hex,
                                           self.id,
                                           self.body)

    def format_detail(self):
        detail = {
            #"id": self.id,
            #"danmaku_uuid": self.danmaku_id.hex,
            #"owner": (self.owner and self.owner.format_detail()) or None,
            "text": self.body,
            #"spoiler": self.spoiler,
            #"style": json.loads(self.style),
            "stime": self.start_time*1000,
            #"create_time": self.create_time.isoformat(),
        }
        detail["mode"] = 1
        detail["size"] = 25
        detail["color"] = 0xffffff
        return detail


class File(Base):
    __tablename__ = 'file'
    hashcode = Column(CHAR(32),
                      primary_key=True)

    danmaku_id = Column(GUID(), ForeignKey('danmaku.id'), index=True)
    danmaku = relationship("Danmaku",
                           backref=backref("file",
                                           lazy="noload",
                                           cascade="all, delete-orphan"),
                           lazy="subquery")

    def __init__(self, hashcode, danmaku):
        self.hashcode = hashcode
        self.danmaku = danmaku

    def __repr__(self):
        return "<File: %s, %s>" % (self.danmaku.name, self.hashcode)

    def format_detail(self):
        detail = {
            "hashcode": self.hashcode,
            "danmaku": self.danmaku.format_detail(),
        }
        return detail


class YoukuVideo(Base):
    __tablename__ = 'youku_video'
    vid = Column(Integer,
                 primary_key=True)
    vid_encoded = Column(CHAR(64),
                         index=True)

    danmaku_id = Column(GUID(), ForeignKey('danmaku.id'), index=True)
    danmaku = relationship("Danmaku",
                           backref=backref("youku_video",
                                           lazy="noload",
                                           cascade="all, delete-orphan"),
                           lazy="subquery")

    def __init__(self, vid, vid_encoded, danmaku):
        self.vid = vid
        self.vid_encoded = vid_encoded
        self.danmaku = danmaku

    def __repr__(self):
        return "<YoukuVideo: %s, %d>" % (self.danmaku.name, self.vid)

    def format_detail(self):
        detail = {
            "vid": str(self.vid),
            "vidEncoded": self.vid_encoded,
            "danmaku": self.danmaku.format_detail(),
        }
        return detail
