# -*- coding: utf-8 -*-
import mongoengine
from fastapi import Body, HTTPException, Request
from fastapi_sso.sso.base import OpenID, SSOBase
from fastapi_sso.sso.google import GoogleSSO

from src.models import User

from . import config


class PasswordSSO(SSOBase):
    provider = 'password'

    async def verify_and_process(self, username: str, password: str):
        # GET user by username from db
        if not (user := User.objects.only(
            'password',
        ).filter(
            username=username,
        ).first()):
            raise HTTPException(status_code=403)

        if password != user.password:
            raise HTTPException(status_code=403)

        return user

    async def verify_and_register(self, username: str, password: str):
        try:
            user = User.objects.create(
                username=username,
                password=password,
            )
        except mongoengine.errors.NotUniqueError as err:
            raise HTTPException(status_code=403) from err

        return user

def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        config.SSO_GOOGLE_CLIENT_ID,
        config.SSO_GOOGLE_CLIENT_SECRET,
        config.SSO_GOOGLE_CALLBACK_URL,
    )

def get_password_sso() -> PasswordSSO:
    return PasswordSSO(
        client_id=None,
        client_secret=None,
    )
