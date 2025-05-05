# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.cache import cache, caches


def app_cache():
    return caches["persianfonts"] if "persianfonts" in settings.CACHES else cache


def del_cached_active_font():
    app_cache().delete("persianfonts_font")


def get_cached_active_font():
    return app_cache().get("persianfonts_font", None)


def set_cached_active_font(font):
    app_cache().set("persianfonts_font", font)
