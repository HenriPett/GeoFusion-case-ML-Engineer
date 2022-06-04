"""Arquivo principal inicializa o app e recebe as rotas correspondentes"""
import os
import json
import uvicorn
from fastapi import FastAPI
from dotenv import find_dotenv, load_dotenv

from core.configuracao import DevSettings, ProdSettings
from services.gera_info import obtem_pois, obtem_predicao
from middleware.verifica import verifica_lat_lgn

app = FastAPI()

DESCRIPTION = """
Geofusion API
"""


def configure_app():
    """Configura o app com base no ambiente"""
    load_dotenv(find_dotenv())
    if os.environ.get("API_ENVIRONMENT") == "prod":
        app_settings = ProdSettings()
    else:
        app_settings = DevSettings()

    fast_api_instance = FastAPI(
        title=app_settings.APP_TITLE, description=DESCRIPTION, version=app_settings.VERSION
    )

    return fast_api_instance, app_settings


app, settings = configure_app()


@app.get("/predict/")
def consulta(lat, lng):
    """
    Endpoint que corresponde ao PATH /predict e responde ao metodo
    GET. Recebe como parametro a latitude e longitude e retorna
    os parametros rerebidos, a predição do modelo e pequenos
    varejistas/grandes redes em um raio de 50 metros
    """
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
