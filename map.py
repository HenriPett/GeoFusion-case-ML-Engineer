from shapely.wkt import loads

with open('campinas.wkt') as f:
    content = f.read()

loads(content)
