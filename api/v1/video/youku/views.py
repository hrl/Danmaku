import json
import uuid

from urllib.parse import (
    urlencode,
    urlparse,
    parse_qs,
)

from tornado import gen

import util
import models
from settings import cache_settings
from ... import base
from . import forms


__all__ = [
    "YoukuVideoHandler",
]


class YoukuVideoHandler(base.APIBaseHandler):
    """
    URL: /youku_videos/(?P<vid>[0-9]+)
    Allowed methods: GET
    """
    def get(self, vid):
        """
        Check video's detail.
        """
        self.finish_object(models.YoukuVideo,
                           int(vid))
