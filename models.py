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
