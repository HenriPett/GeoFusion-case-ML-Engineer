import os
import json
import uvicorn
from fastapi import FastAPI

from core.settings import DevSettings, ProdSettings
from dotenv import find_dotenv, load_dotenv

app = FastAPI()

description = """
Geofusion API
"""


def configure_app():
    load_dotenv(find_dotenv())
    if os.environ.get("API_ENVIRONMENT") == "prod":
        settings = ProdSettings()
    else:
        settings = DevSettings()

    app = FastAPI(
        title=settings.APP_TITLE, description=description, version=settings.VERSION
    )

    return app, settings


app, settings = configure_app()


@app.get("/predict/lat={lat}&lgn={lgn}")
def consult_fiducia(lat, lgn):

    response = {"statusCode": 200, "body": {
        "response": f"{lat}:{lgn}"
    }}

    return json.dumps(response)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
