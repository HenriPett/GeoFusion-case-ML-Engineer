from shapely.wkt import loads
from shapely.geometry import Point

def verifica_lat_lgn(lat, lng):

    with open('campinas.wkt') as f:
        content = f.read()

    map = loads(content)
    point = Point(lng, lat)

    if map.intersection(point):
        return True
    else:
        return False
