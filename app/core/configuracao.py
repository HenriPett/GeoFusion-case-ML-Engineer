"""Arquivo de configurações do app"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Configurações baisicas do app
    """
    VERSION = "0.1.0"
    APP_TITLE = "Geofusion API"


class DevSettings(Settings):
    """
    Configurações do app em ambiente de desenvolvimento
    """
    SERVER_HOST = "0.0.0.0"
    DEBUG = True
    PORT = 8000
    RELOAD = True
    CORS = {
        "origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }


class ProdSettings(Settings):
    """
    Configurações do app em ambiente de produção
    """
    SERVER_HOST = "mydomain.com"
    DEBUG = False
    PORT = 8000
    RELOAD = False
    CORS = {
        "origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
