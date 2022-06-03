import os
import json
import uvicorn
from fastapi import FastAPI

from core.settings import DevSettings, ProdSettings
from services.predict import obtem_pois
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


@app.get("/predict/")
def consult(lat, lng):
    data = {"statusCode": 200, "body": {
        "latitude": lat,
        "longitude": lng,
        "predicao": ''
    }}

    data.update(obtem_pois(float(lat), float(lng)))

    response = data

    return json.dumps(response)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
