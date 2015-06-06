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
    "DanmakusHandler",
    "DanmakuHandler",
]


class DanmakusHandler(base.APIBaseHandler):
    """
    URL: /danmakus
    Allowed methods: GET
    """
    @gen.coroutine
    def get(self):
        """
        Query danmaku pools.
        """
        form = forms.DanmakusForm(self.request.arguments,
                                  locale_code=self.locale.code)
        if form.validate():
            danmakus_query = self.session.query(models.Danmaku)
            danmakus_query = self.apply_order(danmakus_query, form)
            if form.key.data:
                danmakus_query = danmakus_query.filter(
                    models.Danmaku.name.like("%"
                                             + form.key.data.strip().split()[0]
                                             + "%")
                )
            danmakus = danmakus_query.all()

            response = list()
            for danmaku in danmakus:
                response.append(
                    danmaku.format_detail()
                )
            self.finish(json.dumps(response))
        else:
            self.validation_error(form)


class DanmakuHandler(base.APIBaseHandler):
    """
    URL: /danmakus/(?P<id>[0-9a-fA-F]{32})
    Allowed methods: GET
    """
    def get(self, id):
        """
        Check danmaku pool's detail.
        """
        self.finish_object(models.Danmaku,
                           id)
