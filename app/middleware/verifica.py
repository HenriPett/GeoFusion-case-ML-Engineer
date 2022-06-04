"""Arquivo de verificações do controller"""
from shapely.wkt import loads
from shapely.geometry import Point


def verifica_lat_lgn(lat, lng):
    """Verifica se latitude e longitude estão dentro do mapa de campinas"""
    with open('campinas.wkt') as file:
        content = file.read()

    campinas_map = loads(content)
    point = Point(lng, lat)

    if campinas_map.intersection(point):
        return True

    return False
