# -*- coding: utf-8 -*-
from . import application as app


@app.get('/auth/refresh')
def refresh_token():
    return "refresh token"
