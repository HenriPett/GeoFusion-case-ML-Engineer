"""Arquivo responsavel por gerar informações necessarias (POIs e predição) para o usuário"""
import os
from functools import partial
from collections import Counter
import pickle
import pandas as pd
import pyproj
from shapely.ops import transform
from shapely.geometry import Point


df_pois = pd.read_csv(os.path.join(
    os.path.dirname(__file__), '../requirements/pois.csv'))


def gera_isocota(ponto, raio):
    """
    Gera a isocota
    """
    raio_ponto_de_estudo_utm = lat_lng_to_utm(ponto).buffer(raio)
    raio_ponto_de_estudo_lat_lng = utm_to_lat_lng(raio_ponto_de_estudo_utm)
    return raio_ponto_de_estudo_lat_lng


def lat_lng_to_utm(lat_lng_geom):
    """
    Converte uma geometria de latitude e longitude para UTM
    """
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(init='epsg:3857'))
    utm_geom = transform(project, lat_lng_geom)
    return utm_geom


def utm_to_lat_lng(utm_geom):
    """
    Converte uma geometria de UTM para latitude e longitude
    """
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:3857'),
        pyproj.Proj(init='epsg:4326'))
    lat_lng_geom = transform(project, utm_geom)
    return lat_lng_geom


def obtem_configuracao():
    """
    Obtem campos especificos (POIs)
    """
    return {'faculdades', 'escolas', 'ponto_de_onibus', 'concorrentes__grandes_redes',
            'concorrentes__pequeno_varejista', 'minhas_lojas', 'agencia_bancaria', 'padaria',
            'acougue', 'restaurante', 'correio', 'loterica'}


def obtem_pois(latitude: float, longitude: float):
    """
    Obtem os pontos de interesse do ponto passado
    """
    target_pois = {}
    data = pd.DataFrame([{'latitude': latitude,
                          'longitude': longitude}])

    try:
        for row in data.itertuples():
            isocota = gera_isocota(Point(row.longitude, row.latitude), 49)
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

        return {'n_pequeno_varejista': f'{float(df_data.iloc[0].concorrentes__pequeno_varejista)}',
                'n_grandes_redes': f'{float(df_data.iloc[0].concorrentes__grandes_redes)}'}
    except Exception:
        return {'n_pequeno_varejista': '0.0',
                'n_grandes_redes': '0.0'}


def obtem_predicao(latitude: float, longitude: float):
    """
    Obtem a predição do modelo com base no ponto passado
    """
    model = pickle.load(open(os.path.join(
        os.path.dirname(__file__), '../requirements/model_campifarma.pickle'), 'rb'))

    target_pois = {}
    data = pd.DataFrame([{'latitude': latitude,
                          'longitude': longitude}])

    for row in data.itertuples():
        lat, lng = row.latitude, row.longitude
        point = Point(lng, lat)
        isocota = gera_isocota(point, 1000)
        min_lng, min_lat, max_lng, max_lat = isocota.bounds
        mask = (df_pois.latitude.between(min_lat, max_lat) &
                df_pois.longitude.between(min_lng, max_lng))
        counter = Counter()
        for row_poi in df_pois.loc[mask].itertuples():
            if Point(row_poi.longitude, row_poi.latitude).within(isocota):
                counter.update([row_poi.tipo_POI])
        target_pois[row.Index] = counter

    new_row = pd.DataFrame.from_dict(target_pois, orient='Index').fillna(0)
    for i in obtem_configuracao():
        if i not in new_row:
            new_row[i] = 0
# -----------------------------------------------------------------------------------
    dic_enriquecido = {}
    target = 'minhas_lojas'
    area_de_influencia = 1000
    for row_target in df_pois.loc[df_pois['tipo_POI'] == target].itertuples():
        lat, lng = row_target.latitude, row_target.longitude
        point = Point(lng, lat)
        isocota = gera_isocota(point, area_de_influencia)
        min_lng, min_lat, max_lng, max_lat = isocota.bounds
        mask = (df_pois.latitude.between(min_lat, max_lat) &
                df_pois.longitude.between(min_lng, max_lng))
        counter = Counter()
        for row_poi in df_pois.loc[mask].itertuples():
            if Point(row_poi.longitude, row_poi.latitude).within(isocota):
                counter.update([row_poi.tipo_POI])
        dic_enriquecido[row_target.Index] = counter
    df_data = pd.DataFrame.from_dict(dic_enriquecido, orient='Index').fillna(0)

    for i in obtem_configuracao():
        if i not in df_data:
            df_data[i] = 0

    new_df = df_data.append(new_row, ignore_index=True, sort=True)

    return {'predicao': model.predict(new_df)[-1]}
