apps = [
]

urls = [
    (r"/user/register", "user.RegisterHandler"),
    (r"/user/login", "user.LoginHandler"),
    (r"/user", "user.ProfileHandler"),
    (r"/danmakus", "danmaku.DanmakusHandler"),
    (r"/danmakus/(?P<id>[0-9a-fA-F]{32})", "danmaku.DanmakuHandler"),
    (r"/files/(?P<hashcode>[0-9a-fA-F]{32})", "file.FileHandler"),
    (r"/videos/youku/(?P<vid>[0-9]+)", "video.youku.YoukuVideoHandler"),
    (r"/danmakus/(?P<id>[0-9a-fA-F]{32})/tsukkomis", "danmaku.DanmakuTsukkomisHandler"),
    (r"/danmakus/(?P<id>[0-9a-fA-F]{32})/tsukkomis/ws", "danmaku.DanmakuTsukkomisWSHandler"),
]
