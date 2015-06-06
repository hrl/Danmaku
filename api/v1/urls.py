apps = [
]

urls = [
    (r"/user/register", "user.RegisterHandler"),
    (r"/user/login", "user.LoginHandler"),
    (r"/user", "user.ProfileHandler"),
    (r"/danmakus", "danmaku.DanmakusHandler"),
    (r"/danmakus/(?P<id>[0-9a-fA-F]{32})", "danmaku.DanmakuHandler"),
]
