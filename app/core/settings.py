from pydantic import BaseSettings


class Settings(BaseSettings):
    VERSION = "0.1.0"
    APP_TITLE = "Geofusion API"


class DevSettings(Settings):
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
