import json
import uuid

from urllib.parse import (
    urlencode,
    urlparse,
    parse_qs,
)

from tornado import gen

from pyquery.pyquery import PyQuery

import util
import models
from settings import cache_settings
from .. import base
from . import forms


__all__ = [
    "FileHandler",
]


class FileHandler(base.APIBaseHandler):
    """
    URL: /files/(?P<hashcode>[0-9a-fA-F]{32})
    Allowed methods: GET
    """
    def get(self, hashcode):
        """
        Check file's detail.
        """
        self.finish_object(models.File,
                           hashcode.lower())
