from fastapi import FastAPI

from src import auth, features

app = FastAPI()
app.include_router(auth.router)
app.include_router(features.social.router)

@app.get('/debug')
def debug():
    return 'hello'
