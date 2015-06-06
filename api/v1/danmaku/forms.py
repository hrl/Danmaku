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
