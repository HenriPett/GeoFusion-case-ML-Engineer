import pandas as pd
import pyproj
from functools import partial
from shapely.ops import transform
from collections import Counter
from shapely.geometry import Point
import pickle

loaded_model = pickle.load(open('model_campifarma.pickle', 'rb'))
df_pois = pd.read_csv('pois.csv')


def gera_isocota(ponto, raio):
    raio_ponto_de_estudo_utm = lat_lng_to_utm(ponto).buffer(raio)
    raio_ponto_de_estudo_lat_lng = utm_to_lat_lng(raio_ponto_de_estudo_utm)
    return raio_ponto_de_estudo_lat_lng


def lat_lng_to_utm(lat_lng_geom):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),  # source coordinate system
        pyproj.Proj(init='epsg:3857'))  # destination coordinate system
    utm_geom = transform(project, lat_lng_geom)
    return utm_geom


def utm_to_lat_lng(utm_geom):
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:3857'),  # source coordinate system
        pyproj.Proj(init='epsg:4326'))  # destination coordinate system
    lat_lng_geom = transform(project, utm_geom)
    return lat_lng_geom


def obtem_configuracao():
    return {'faculdades', 'escolas', 'ponto_de_onibus', 'concorrentes__grandes_redes',
            'concorrentes__pequeno_varejista', 'minhas_lojas', 'agencia_bancaria', 'padaria',
            'acougue', 'restaurante', 'correio', 'loterica'}


def obtem_pois(latitude: float, longitude: float):

    area_de_influencia = 50
    target_pois = {}
    data = pd.DataFrame([{'latitude': latitude,
                          'longitude': longitude}])

    try:
        for row in data.itertuples():
            lat, lng = row.latitude, row.longitude
            pt = Point(lng, lat)
            isocota = gera_isocota(pt, area_de_influencia)
            min_lng, min_lat, max_lng, max_lat = isocota.bounds
            mask = (df_pois.latitude.between(min_lat, max_lat) &
                    df_pois.longitude.between(min_lng, max_lng))
            counter = Counter()
            for row_poi in df_pois.loc[mask].itertuples():
                if Point(row_poi.longitude, row_poi.latitude).within(isocota):
                    counter.update([row_poi.tipo_POI])
            target_pois[row.Index] = counter

        df_data = pd.DataFrame.from_dict(target_pois, orient='Index').fillna(0)
        for i in obtem_configuracao():
            if i not in df_data:
                df_data[i] = 0

        return {'n_pequeno_varejista': f'{df_data.iloc[0].concorrentes__pequeno_varejista}',
                'n_grandes_redes': f'{df_data.iloc[0].concorrentes__grandes_redes}'}
    except Exception as e:
        print(e)
        return {'n_pequeno_varejista': '0',
                'n_grandes_redes': '0'}


def obtem_data(latitude: float, longitude: float):

    area_de_influencia = 1000
    target_pois = {}
    data = pd.DataFrame([{'latitude': latitude,
                          'longitude': longitude}])

    for row in data.itertuples():
        lat, lng = row.latitude, row.longitude
        pt = Point(lng, lat)
        isocota = gera_isocota(pt, area_de_influencia)
        min_lng, min_lat, max_lng, max_lat = isocota.bounds
        mask = (df_pois.latitude.between(min_lat, max_lat) &
                df_pois.longitude.between(min_lng, max_lng))
        counter = Counter()
        for row_poi in df_pois.loc[mask].itertuples():
            if Point(row_poi.longitude, row_poi.latitude).within(isocota):
                counter.update([row_poi.tipo_POI])
        target_pois[row.Index] = counter

    df_data = pd.DataFrame.from_dict(target_pois, orient='Index').fillna(0)
    for i in obtem_configuracao():
        if i not in df_data:
            df_data[i] = 0

    return loaded_model.predict(df_data)


print(obtem_data(-22.818201, -46.988467))
