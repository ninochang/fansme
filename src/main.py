# -*- coding: utf-8 -*-
import mongoengine
from fastapi import FastAPI

from src import auth, config, features

app = FastAPI()
app.include_router(auth.router)
app.include_router(features.social.router)

db = mongoengine.connect(db='fansme', host=config.MONGODB_URL)

@app.get('/debug')
def debug():
    return 'hello'
