from form import Form
from wtforms.fields import (
    Field,
    IntegerField,
    StringField,
    SelectField,
)
from wtforms.validators import (
    ValidationError,
    StopValidation,
    InputRequired,
    EqualTo,
    Length,
)
from wtforms.ext.dateutil.fields import DateTimeField

import models
from .. import baseForms
from .. import baseValidators


class DanmakusForm(Form, baseForms.SliceMixin):
    """
    Used in:
        danmaku.DanmakusHandler
            method=['GET']
            Query danmaku pools.
    """
    sortby = SelectField('sortby', default="name", choices=[
        ("create_time", "cerate_time"),
        ("name", "name"),
    ])
    order = SelectField('order', default="desc", choices=[
        ("asc", "asc"),
        ("desc", "desc"),
    ])
    key = StringField('key', default="")


class DanmakuTsukkomisWSForm(Form, baseForms.SliceMixin):
    """
    Used in:
        danmaku.DanmakuTsukkomisWSHandler
            method=['subscribe']
            Subscribe tsukkomis.
    """
    danmaku = Field('danmaku', [
        baseValidators.danmaku_get,
    ])
    dateafter = DateTimeField('dateafter')

    sortby = SelectField('sortby', default="create_time", choices=[
        ("create_time", "cerate_time"),
    ])
    order = SelectField('order', default="desc", choices=[
        ("desc", "desc"),
    ])


class DanmakuTsukkomisForm(Form):
    """
    Used in:
        danmaku.DanmakuTsukkomisHandler
            method=['POST']
            Tsukkomi.
    """
    danmaku = Field('danmaku', [
        baseValidators.danmaku_get,
    ])
    body = StringField('body', [
        InputRequired(),
    ])
    style = Field('style')
    start_time = IntegerField('start_time', default=0)
    spoiler = Field('spoiler', [
        baseValidators.boolean_check,
    ])
