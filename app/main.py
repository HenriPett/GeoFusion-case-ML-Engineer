import os
import json
import uvicorn
from fastapi import FastAPI

from core.settings import DevSettings, ProdSettings
from services.predict import obtem_pois, obtem_predicao
from middleware.verifica import verifica_lat_lgn
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
    if not verifica_lat_lgn(float(lat), float(lng)):
        return json.dumps({'status_code': 401,
                           'body': {
                               "latitude": lat,
                               "longitude": lng,
                               'predicao': '-1',
                               'n_pequeno_varejista': '-1',
                               'n_grandes_redes': '-1',
                           }
                           })

    data = {
        "latitude": lat,
        "longitude": lng,
    }

    data.update(obtem_pois(float(lat), float(lng)))
    data.update(obtem_predicao(float(lat), float(lng)))

    response = {'status_code': 200, 'body': data}

    return json.dumps(response)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )
