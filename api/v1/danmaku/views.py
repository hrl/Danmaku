import json
import uuid

from urllib.parse import (
    urlencode,
    urlparse,
    parse_qs,
)

from tornado import gen

import tornadoredis

import util
import database
import models
from settings import cache_settings
from .. import base
from . import forms

trediscli_co = tornadoredis.Client()
trediscli_co.connect()


__all__ = [
    "DanmakusHandler",
    "DanmakuHandler",
    "DanmakuTsukkomisWSHandler",
    "DanmakuTsukkomisHandler",
]


class DanmakusHandler(base.APIBaseHandler):
    """
    URL: /danmakus
    Allowed methods: GET
    """
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


class DanmakuTsukkomisWSHandler(base.WebSocketAPIHandler, base.QueryHandlerMixin):
    """
    URL: /danmakus/(?P<id>[0-9a-fA-F]{32})/tsukkomis/ws
    Allowed methods: subscribe
    """
    def check_origin(self, origin):
        return True

    def open(self, id):
        self.ws_methods = [
            "subscribe"
        ]
        self.danmaku_id = id
        self.session = database.db_session()

    def on_close(self):
        self.session.close()

    def close_tredis(self):
        try:
            self.trediscli.unsubscribe('danmaku:%s' % self.danmaku_id)
            self.trediscli.close()
        except Exception:
            pass

    def connect_tredis(self):
        self.close_tredis()
        self.trediecli = tornadoredis.Client()
        self.trediecli.connect()


    @gen.coroutine
    def subscribe(self, message):
        def tredis_on_message(msg):
            if msg.kind == 'message':
                self.write_ws_response(message.get('id'),
                                       str(msg.body),
                                       200)
            if msg.kind == 'disconnect':
                raise base.WebSocketAPIError(500)

        form = forms.DanmakuTsukkomisWSForm(message['body'],
                                            locale_code=self.locale.code,
                                            danmaku=self.danmaku_id)
        if form.validate():
            tsukkomis_query = form.danmaku.data.tsukkomi
            if form.dateafter.data:
                tsukkomis_query = tsukkomis_query.filter(
                    models.Tsukkomi.create_time > form.dateafter.date
                )
            tsukkomis_query = self.apply_order(tsukkomis_query, form)
            tsukkomis = tsukkomis_query.all()

            response = list()
            for tsukkomi in tsukkomis:
                response.append(
                    tsukkomi.format_detail()
                )
            self.write_ws_response(message.get('id'), json.dumps(response), 200)

            # subscribe
            self.connect_tredis()
            yield gen.Task(self.trediecli.subscribe,
                           ('danmaku:%s' % self.danmaku_id,))
            self.trediecli.listen(tredis_on_message)
        else:
            self.validation_error(form)


class DanmakuTsukkomisHandler(base.APIBaseHandler):
    """
    URL: /danmakus/(?P<id>[0-9a-fA-F]{32})/tsukkomis
    Allowed methods: POST
    """
    def post(self, id):
        form = forms.DanmakuTsukkomisForm(self.json_args,
                                          locale_code=self.locale.code,
                                          danmaku=id)
        if form.validate():
            tsukkomi = self.create_tsukkomi(form)
            result_json = json.dumps(tsukkomi.format_detail())
            trediscli_co.publish('danmaku:%s' % form.danmaku.data.id.hex,
                                 result_json)
            self.set_status(201)
            self.finish(result_json)
        else:
            self.validation_error(form)

    @base.db_success_or_500
    def create_tsukkomi(self, form):
        danmaku = form.danmaku.data
        tsukkomi = models.Tsukkomi(
            danmaku=danmaku,
            body=form.body.data,
            style=form.style.data,
            start_time=form.start_time.data,
            spoiler=form.spoiler.data,
            owner=self.current_user,
        )
        self.session.add(tsukkomi)
        return tsukkomi
